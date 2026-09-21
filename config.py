import os
from dataclasses import dataclass


def _get_env(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name)
        if value is not None and value.strip():
            return value.strip()
    return default


def _get_bool(*names: str, default: bool = False) -> bool:
    return _get_env(*names, default=str(default)).lower() in {"1", "true", "yes", "on"}


def _get_int(*names: str, default: int = 0) -> int:
    try:
        return int(_get_env(*names, default=str(default)))
    except ValueError:
        return default


@dataclass(frozen=True)
class AppConfig:
    app_name: str = _get_env("APP_NAME", "ENGINE_NAME", default="Sovereign Master AI")
    engine_name: str = _get_env("ENGINE_NAME", "APP_NAME", default="Sovereign Master AI")
    engine_version: str = _get_env("APP_VERSION", "ENGINE_VERSION", default="2.0.0")
    environment: str = _get_env("APP_ENV", "ENVIRONMENT", default="development")
    host: str = _get_env("HOST", default="0.0.0.0")
    port: int = _get_int("PORT", default=8000)
    database_url: str = _get_env("DATABASE_URL", default="")
    postgres_sslmode: str = _get_env("POSTGRES_SSLMODE", default="require")
    pgvector_enabled: bool = _get_bool("PGVECTOR_ENABLED", default=True)
    vector_dimension: int = _get_int("VECTOR_DIMENSION", default=1536)
    model_provider: str = _get_env("AI_PROVIDER", "MODEL_PROVIDER", default="local_fallback")
    model_name: str = _get_env("AI_MODEL", "MODEL_NAME", default="")
    model_api_key: str = _get_env("AI_API_KEY", "MODEL_API_KEY", default="")
    model_base_url: str = _get_env("AI_BASE_URL", "MODEL_BASE_URL", default="")
    voice_enabled: bool = _get_bool("VOICE_ENABLED", default=False)
    voice_provider: str = _get_env("VOICE_PROVIDER", default="")
    voice_profile_id: str = _get_env("VOICE_PROFILE_ID", default="")
    admin_secret: str = _get_env("SECRET_KEY", "ADMIN_SECRET", default="change-me")
    admin_username: str = _get_env("ADMIN_USERNAME", default="admin")
    admin_token: str = _get_env("ADMIN_API_KEY", "ADMIN_TOKEN", default="")
    brand_name: str = _get_env("BRAND_NAME", default="PROPHÈTE KESMANER HENRY")
    default_language: str = _get_env("DEFAULT_LANGUAGE", default="auto")
    supported_languages: tuple[str, ...] = tuple(_get_env("SUPPORTED_LANGUAGES", default="ht,fr,en").split(","))
    safety_enabled: bool = _get_bool("SAFETY_ENABLED", default=True)
    media_safety_enabled: bool = _get_bool("MEDIA_SAFETY_ENABLED", default=True)
    human_review_enabled: bool = _get_bool("HUMAN_REVIEW_ENABLED", default=True)
    log_level: str = _get_env("LOG_LEVEL", default="INFO")
    structured_logging: bool = _get_bool("STRUCTURED_LOGGING", default=True)


CONFIG = AppConfig()
