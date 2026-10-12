"""Asli web app and API."""

from __future__ import annotations

import asyncio
import hashlib
import logging
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, Request, Response, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from . import i18n, ocr
from .analysis.engine import check
from .analysis.redact import redact
from .config import Settings
from .db import Store
from .ratelimit import RateLimiter
from .whatsapp import WhatsAppClient, format_reply, incoming, valid_signature

log = logging.getLogger("asli")
HERE = Path(__file__).resolve().parent

EXAMPLES = {
    "kyc": "Dear customer, your SBI YONO account will be blocked today. Update your PAN card immediately: http://sbi-kyc-update.xyz/login",
    "job": "Hi, part time job available! Earn Rs 3000 daily by liking YouTube videos. Ghar baithe kamaye. Contact HR on Telegram t.me/hr_priya",
    "otp": "482913 is your OTP for transaction of Rs 1,250 at Amazon. Valid for 10 mins. Do not share it with anyone. -HDFC Bank",
}


class CheckIn(BaseModel):
    text: str = Field(min_length=1, max_length=4000)
    lang: str | None = None


class FeedbackIn(BaseModel):
    check_id: str = Field(min_length=36, max_length=36)
    correct: bool


def pick_lang(request: Request, explicit: str | None = None) -> str:
    for cand in (explicit, request.query_params.get("lang"), request.cookies.get("lang")):
        if cand in i18n.LANGS:
            return cand
    accept = request.headers.get("accept-language", "").lower()
    for code in ("kn", "hi"):
        if accept.startswith(code) or f",{code}" in accept.replace(" ", ""):
            return code
    return "en"


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    app = FastAPI(title="Asli", version="1.0.0", docs_url="/api/docs", redoc_url=None)
    app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
    templates = Jinja2Templates(directory=HERE / "templates")
    store = Store(settings.database_url)
    limiter = RateLimiter(settings.rate_limit_per_minute)
    wa = WhatsAppClient(settings) if settings.whatsapp_enabled else None
    app.state.settings, app.state.store = settings, store

    def client_key(request: Request) -> str:
        ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "?").split(",")[0].strip()
        return hashlib.sha256((settings.hash_salt + ip).encode()).hexdigest()[:24]

    def run_check(text: str, lang: str | None, channel: str) -> dict:
        report = check(text[: settings.max_message_chars], lang)
        if settings.store_checks:
            try:
                report["check_id"] = store.save_check(channel=channel, report=report, redacted=redact(report["text"]))
            except Exception:  # storage must never block a warning reaching the person
                log.exception("could not store check")
        return report

    # --- pages ---------------------------------------------------------------

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request):
        lang = pick_lang(request)
        resp = templates.TemplateResponse(request, "index.html", {
            "lang": lang, "t": i18n.UI[lang], "langs": i18n.LANGS, "examples": EXAMPLES,
            "ocr": ocr.available(), "wa_number": settings.whatsapp_display_number,
        })
        resp.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365, samesite="lax")
        return resp

    @app.get("/healthz")
    def health():
        return {"ok": True, "ocr": ocr.available(), "whatsapp": settings.whatsapp_enabled}

    # --- API -------------------------------------------------------------------

    @app.post("/api/check")
    def api_check(body: CheckIn, request: Request):
        if not limiter.allow(client_key(request)):
            raise HTTPException(429, i18n.UI[pick_lang(request, body.lang)]["too_many"])
        return run_check(body.text, pick_lang(request, body.lang), "web")

    @app.post("/api/check-image")
    async def api_check_image(request: Request, image: UploadFile = File(...), lang: str | None = Form(None)):
        ui = i18n.UI[pick_lang(request, lang)]
        if not limiter.allow(client_key(request)):
            raise HTTPException(429, ui["too_many"])
        if not ocr.available():
            raise HTTPException(503, "Screenshot reading is not available on this server.")
        data = await image.read(settings.max_image_bytes + 1)
        if len(data) > settings.max_image_bytes:
            raise HTTPException(413, "Images must be under 5 MB.")
        try:
            text = await asyncio.to_thread(ocr.image_to_text, data)
        except Exception:
            raise HTTPException(422, ui["no_text"])
        if len(text.strip()) < 4:
            raise HTTPException(422, ui["no_text"])
        return run_check(text, pick_lang(request, lang), "web-image")

    @app.post("/api/feedback")
    def api_feedback(body: FeedbackIn):
        if not store.save_feedback(body.check_id, body.correct):
            raise HTTPException(404, "Unknown check")
        return {"ok": True}

    @app.get("/api/stats")
    def api_stats():
        return store.stats()

    # --- WhatsApp --------------------------------------------------------------

    @app.get("/webhooks/whatsapp")
    def wa_verify(request: Request):
        q = request.query_params
        if (q.get("hub.mode") == "subscribe" and settings.whatsapp_verify_token
                and q.get("hub.verify_token") == settings.whatsapp_verify_token):
            return PlainTextResponse(q.get("hub.challenge", ""))
        raise HTTPException(403, "Verification failed")

    @app.post("/webhooks/whatsapp")
    async def wa_receive(request: Request, background: BackgroundTasks):
        if wa is None:
            raise HTTPException(503, "WhatsApp is not configured")
        body = await request.body()
        if not valid_signature(settings, body, request.headers.get("x-hub-signature-256")):
            raise HTTPException(401, "Bad signature")
        for msg in incoming(await request.json()):
            background.add_task(handle_whatsapp, msg)
        return Response(status_code=200)  # Meta retries anything that isn't a fast 200

    async def handle_whatsapp(msg: dict) -> None:
        sender_key = hashlib.sha256((settings.hash_salt + msg["from"]).encode()).hexdigest()[:24]
        try:
            text = msg["text"]
            if msg["type"] == "image" and msg["media_id"] and ocr.available():
                data = await wa.download_media(msg["media_id"], settings.max_image_bytes)
                text = (text + " " + await asyncio.to_thread(ocr.image_to_text, data)).strip()
            if msg["type"] not in ("text", "image") or not text:
                await wa.send_text(msg["from"], i18n.UI["en"]["empty"], msg["id"])
                return
            report = check(text[: settings.max_message_chars])
            lang = report["language"]
            if not limiter.allow(sender_key):
                await wa.send_text(msg["from"], i18n.UI[lang]["too_many"], msg["id"])
                return
            if settings.store_checks:
                store.save_check(channel="whatsapp", report=report, redacted=redact(report["text"]))
            await wa.send_text(msg["from"], format_reply(report, i18n.UI[lang]), msg["id"])
        except Exception:
            log.exception("whatsapp handling failed")

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException):
        return JSONResponse({"error": exc.detail}, status_code=exc.status_code)

    return app


app = create_app()
