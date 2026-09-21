import os
from dataclasses import dataclass


def _get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


@dataclass(frozen=True)
class AppConfig:
    app_name: str = "Sovereign Master AI"
    engine_name: str = _get_env("ENGINE_NAME", "Sovereign Master AI")
    engine_version: str = _get_env("ENGINE_VERSION", "0.1.0")
    environment: str = _get_env("ENVIRONMENT", "development")
    port: int = int(_get_env("PORT", "8080"))
    database_url: str = _get_env("DATABASE_URL", "")
    model_provider: str = _get_env("MODEL_PROVIDER", "local_fallback")
    model_name: str = _get_env("MODEL_NAME", "")
    model_api_key: str = _get_env("MODEL_API_KEY", "")
    model_base_url: str = _get_env("MODEL_BASE_URL", "")
    voice_enabled: bool = _get_env("VOICE_ENABLED", "false").lower() == "true"
    voice_provider: str = _get_env("VOICE_PROVIDER", "")
    voice_profile_id: str = _get_env("VOICE_PROFILE_ID", "")
    admin_secret: str = _get_env("ADMIN_SECRET", "change-me")
    admin_username: str = _get_env("ADMIN_USERNAME", "admin")
    admin_token: str = _get_env("ADMIN_TOKEN", "")


CONFIG = AppConfig()
