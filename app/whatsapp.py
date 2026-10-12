"""WhatsApp Cloud API: verify webhooks, parse incoming messages, send replies.

Setup is in the README. Meta signs every webhook POST with the app secret
(X-Hub-Signature-256); unsigned or wrongly signed requests are rejected.
"""

from __future__ import annotations

import hashlib
import hmac

import httpx

from .config import Settings


def valid_signature(settings: Settings, body: bytes, header: str | None) -> bool:
    if not header or not header.startswith("sha256="):
        return False
    expected = hmac.new(settings.whatsapp_app_secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header.split("=", 1)[1])


def incoming(payload: dict) -> list[dict]:
    """Flatten a webhook payload into [{from, id, type, text, media_id}]."""
    out = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            for m in change.get("value", {}).get("messages", []) or []:
                kind = m.get("type")
                item = {"from": m.get("from", ""), "id": m.get("id", ""), "type": kind, "text": "", "media_id": ""}
                if kind == "text":
                    item["text"] = m.get("text", {}).get("body", "")
                elif kind == "image":
                    item["media_id"] = m.get("image", {}).get("id", "")
                    item["text"] = m.get("image", {}).get("caption", "")
                out.append(item)
    return out


def format_reply(report: dict, ui: dict) -> str:
    icon = {"scam": "🚫", "suspicious": "⚠️", "no_signs": "✅"}[report["verdict"]]
    lines = [f"{icon} *{report['headline']}*", ""]
    for f in report["flags"][:4]:
        lines.append(f"• *{f['title']}*\n  {f['detail']}")
    if report["flags"]:
        lines.append("")
    lines.append(f"*{ui['what_to_do']}*")
    lines.extend(f"{i}. {a}" for i, a in enumerate(report["actions"], 1))
    return "\n".join(lines)


class WhatsAppClient:
    def __init__(self, settings: Settings):
        self.s = settings
        self.base = f"https://graph.facebook.com/{settings.graph_api_version}"
        self.headers = {"Authorization": f"Bearer {settings.whatsapp_token}"}

    async def send_text(self, to: str, body: str, reply_to: str | None = None) -> None:
        data = {"messaging_product": "whatsapp", "to": to, "type": "text", "text": {"body": body[:4000]}}
        if reply_to:
            data["context"] = {"message_id": reply_to}
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(f"{self.base}/{self.s.whatsapp_phone_id}/messages", json=data, headers=self.headers)
            r.raise_for_status()

    async def download_media(self, media_id: str, max_bytes: int) -> bytes:
        async with httpx.AsyncClient(timeout=15) as c:
            meta = await c.get(f"{self.base}/{media_id}", headers=self.headers)
            meta.raise_for_status()
            info = meta.json()
            if int(info.get("file_size", 0)) > max_bytes:
                raise ValueError("image too large")
            r = await c.get(info["url"], headers=self.headers)
            r.raise_for_status()
            return r.content
