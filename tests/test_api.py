import hashlib
import hmac
import io
import json
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app import ocr
from app.config import Settings
from app.main import create_app

SCAM = "Dear customer your SBI account will be blocked. Update KYC at http://sbi-kyc.xyz and share OTP 482913. Call 9876543210"


def make_client(tmp_path, **overrides):
    s = Settings()
    s.database_url = f"sqlite:///{tmp_path / 'test.db'}"
    for k, v in overrides.items():
        setattr(s, k, v)
    return TestClient(create_app(s)), s


@pytest.fixture
def client(tmp_path):
    return make_client(tmp_path)[0]


def test_pages_and_health(client):
    for lang in ("en", "hi", "kn"):
        r = client.get(f"/?lang={lang}")
        assert r.status_code == 200 and f'lang="{lang}"' in r.text
    assert client.get("/healthz").json()["ok"] is True


def test_check_stores_redacted_text(client):
    r = client.post("/api/check", json={"text": SCAM, "lang": "en"})
    assert r.status_code == 200
    body = r.json()
    assert body["verdict"] == "scam" and body["check_id"]
    store = client.app.state.store
    from app.db import Check
    with store.session() as s:
        row = s.get(Check, body["check_id"])
    assert "9876543210" not in row.redacted_text and "482913" not in row.redacted_text
    assert "sbi-kyc.xyz" in row.redacted_text


def test_feedback_roundtrip(client):
    cid = client.post("/api/check", json={"text": SCAM}).json()["check_id"]
    assert client.post("/api/feedback", json={"check_id": cid, "correct": True}).json() == {"ok": True}
    assert client.post("/api/feedback", json={"check_id": "0" * 36, "correct": True}).status_code == 404
    assert client.get("/api/stats").json()["feedback"]["correct"] == 1


def test_validation(client):
    assert client.post("/api/check", json={"text": ""}).status_code == 422
    assert client.post("/api/check", json={"text": "x" * 4001}).status_code == 422


def test_rate_limit(tmp_path):
    client, _ = make_client(tmp_path, rate_limit_per_minute=2)
    codes = [client.post("/api/check", json={"text": "hello there friend"}).status_code for _ in range(3)]
    assert codes == [200, 200, 429]


@pytest.mark.skipif(not ocr.available(), reason="tesseract not installed")
def test_image_check(client):
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (1200, 200), "white")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 34)
    except OSError:
        font = ImageFont.load_default()
    d.text((20, 40), "Please share the OTP you received", fill="black", font=font)
    d.text((20, 110), "Your account will be blocked today", fill="black", font=font)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    r = client.post("/api/check-image", files={"image": ("s.png", buf.getvalue(), "image/png")}, data={"lang": "en"})
    assert r.status_code == 200, r.text
    assert r.json()["verdict"] in ("scam", "suspicious")


# --- WhatsApp -------------------------------------------------------------------

def wa_client(tmp_path):
    client, s = make_client(tmp_path, whatsapp_token="t", whatsapp_phone_id="123", whatsapp_app_secret="secret",
                            whatsapp_verify_token="verify-me")
    return client, s


def test_whatsapp_verify(tmp_path):
    client, _ = wa_client(tmp_path)
    ok = client.get("/webhooks/whatsapp", params={"hub.mode": "subscribe", "hub.verify_token": "verify-me", "hub.challenge": "42"})
    assert ok.status_code == 200 and ok.text == "42"
    assert client.get("/webhooks/whatsapp", params={"hub.mode": "subscribe", "hub.verify_token": "nope"}).status_code == 403


def test_whatsapp_rejects_bad_signature(tmp_path):
    client, _ = wa_client(tmp_path)
    r = client.post("/webhooks/whatsapp", content=b"{}", headers={"x-hub-signature-256": "sha256=bad"})
    assert r.status_code == 401


def test_whatsapp_replies(tmp_path, monkeypatch):
    sent = AsyncMock()
    monkeypatch.setattr("app.whatsapp.WhatsAppClient.send_text", sent)
    client, s = wa_client(tmp_path)
    payload = {"entry": [{"changes": [{"value": {"messages": [
        {"from": "919800000000", "id": "wamid.1", "type": "text", "text": {"body": SCAM}}]}}]}]}
    body = json.dumps(payload).encode()
    sig = "sha256=" + hmac.new(b"secret", body, hashlib.sha256).hexdigest()
    r = client.post("/webhooks/whatsapp", content=body, headers={"x-hub-signature-256": sig, "content-type": "application/json"})
    assert r.status_code == 200
    assert sent.await_count == 1
    to, text, reply_to = sent.await_args.args[:3]
    assert to == "919800000000" and reply_to == "wamid.1"
    assert "1930" in text
