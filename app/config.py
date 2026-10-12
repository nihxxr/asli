from __future__ import annotations

import os
from dataclasses import dataclass, field


def _bool(name: str, default: bool) -> bool:
    v = os.environ.get(name)
    return default if v is None else v.strip().lower() in ("1", "true", "yes", "on")


@dataclass
class Settings:
    database_url: str = field(default_factory=lambda: os.environ.get("DATABASE_URL", "sqlite:///./asli.db"))
    store_checks: bool = field(default_factory=lambda: _bool("STORE_CHECKS", True))
    rate_limit_per_minute: int = field(default_factory=lambda: int(os.environ.get("RATE_LIMIT_PER_MINUTE", "20")))
    max_message_chars: int = 4000
    max_image_bytes: int = 5 * 1024 * 1024
    hash_salt: str = field(default_factory=lambda: os.environ.get("HASH_SALT", "change-me"))

    # WhatsApp Cloud API (Meta). Leave empty to disable the webhook.
    whatsapp_token: str = field(default_factory=lambda: os.environ.get("WHATSAPP_TOKEN", ""))
    whatsapp_phone_id: str = field(default_factory=lambda: os.environ.get("WHATSAPP_PHONE_NUMBER_ID", ""))
    whatsapp_verify_token: str = field(default_factory=lambda: os.environ.get("WHATSAPP_VERIFY_TOKEN", ""))
    whatsapp_app_secret: str = field(default_factory=lambda: os.environ.get("WHATSAPP_APP_SECRET", ""))
    whatsapp_display_number: str = field(default_factory=lambda: os.environ.get("WHATSAPP_DISPLAY_NUMBER", ""))
    graph_api_version: str = field(default_factory=lambda: os.environ.get("GRAPH_API_VERSION", "v21.0"))

    @property
    def whatsapp_enabled(self) -> bool:
        return bool(self.whatsapp_token and self.whatsapp_phone_id and self.whatsapp_app_secret)
