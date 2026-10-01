import os
import hmac
import hashlib
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

def _get_env(*names: str, default: str = "") -> str:
    """Get environment variable with fallback names. No hardcoded defaults for secrets."""
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
    # Core configuration
    app_name: str = _get_env("APP_NAME", "ENGINE_NAME", default="Sovereign Master AI")
    engine_name: str = _get_env("ENGINE_NAME", "APP_NAME", default="Sovereign Master AI")
    engine_version: str = _get_env("APP_VERSION", "ENGINE_VERSION", default="2.0.0")
    environment: str = _get_env("APP_ENV", "ENVIRONMENT", default="development")
    host: str = _get_env("HOST", default="0.0.0.0")
    port: int = _get_int("PORT", default=8000)
    
    # Database
    database_url: str = _get_env("DATABASE_URL", default="")
    postgres_sslmode: str = _get_env("POSTGRES_SSLMODE", default="require")
    pgvector_enabled: bool = _get_bool("PGVECTOR_ENABLED", default=True)
    vector_dimension: int = _get_int("VECTOR_DIMENSION", default=1536)
    
    # AI Model Provider
    model_provider: str = _get_env("AI_PROVIDER", "MODEL_PROVIDER", default="local_fallback")
    model_name: str = _get_env("AI_MODEL", "MODEL_NAME", default="")
    model_api_key: str = _get_env("AI_API_KEY", "MODEL_API_KEY", default="")
    model_base_url: str = _get_env("AI_BASE_URL", "MODEL_BASE_URL", default="")
    
    # Voice
    voice_enabled: bool = _get_bool("VOICE_ENABLED", default=False)
    voice_provider: str = _get_env("VOICE_PROVIDER", default="")
    voice_profile_id: str = _get_env("VOICE_PROFILE_ID", default="")
    
    # Admin/Security (non-sovereign)
    admin_secret: str = _get_env("SECRET_KEY", "ADMIN_SECRET", default="change-me")
    admin_username: str = _get_env("ADMIN_USERNAME", default="admin")
    admin_token: str = _get_env("ADMIN_API_KEY", "ADMIN_TOKEN", default="")
    
    # Branding
    brand_name: str = _get_env("BRAND_NAME", default="PROPHÈTE KESMANER HENRY")
    default_language: str = _get_env("DEFAULT_LANGUAGE", default="auto")
    supported_languages: tuple = tuple(_get_env("SUPPORTED_LANGUAGES", default="ht,fr,en").split(","))
    
    # Safety
    safety_enabled: bool = _get_bool("SAFETY_ENABLED", default=True)
    media_safety_enabled: bool = _get_bool("MEDIA_SAFETY_ENABLED", default=True)
    human_review_enabled: bool = _get_bool("HUMAN_REVIEW_ENABLED", default=True)
    
    # Observability
    log_level: str = _get_env("LOG_LEVEL", default="INFO")
    structured_logging: bool = _get_bool("STRUCTURED_LOGGING", default=True)
    
    # ============================================================================
    # 👑 SOVEREIGN MASTER SECURITY - STRICT NO DEFAULT VALUES
    # ============================================================================
    # These MUST be set in deployment environment. No fallback defaults.
    @property
    def system_master_name(self) -> str:
        """Master identity - REQUIRED in production."""
        value = os.getenv("SYSTEM_MASTER_NAME")
        if not value:
            if self.environment == "production":
                raise ValueError("SYSTEM_MASTER_NAME required in production environment")
            return "Prophete-Kesmaner Henry"
        return value
    
    @property
    def assistant_identity(self) -> str:
        """Assistant identity - REQUIRED in production."""
        value = os.getenv("ASSISTANT_IDENTITY")
        if not value:
            if self.environment == "production":
                raise ValueError("ASSISTANT_IDENTITY required in production environment")
            return "GrandArchitect"
        return value
    
    @property
    def master_root_key(self) -> str:
        """Master root key for authorization - REQUIRED in production."""
        value = os.getenv("MASTER_ROOT_KEY")
        if not value:
            if self.environment == "production":
                raise ValueError("MASTER_ROOT_KEY required in production environment")
            return ""
        return value
    
    @property
    def sovereign_openai_core(self) -> str:
        """OpenAI sovereign key - REQUIRED if OpenAI integration is used."""
        return os.getenv("SOVEREIGN_OPENAI_CORE", "")
    
    @property
    def sovereign_gemini_core(self) -> str:
        """Gemini sovereign key - REQUIRED if Gemini integration is used."""
        return os.getenv("SOVEREIGN_GEMINI_CORE", "")
    
    @property
    def grand_architect_key(self) -> str:
        """Grand Architect sovereign key - REQUIRED if Architect module is used."""
        return os.getenv("GRAND_ARCHITECT_KEY", "")

CONFIG = AppConfig()

# Validate critical keys on startup
if CONFIG.environment == "production":
    missing_keys = []
    try:
        _ = CONFIG.master_root_key
        _ = CONFIG.system_master_name
        _ = CONFIG.assistant_identity
    except ValueError as e:
        missing_keys.append(str(e))
    
    if missing_keys:
        logger.error(f"CRITICAL: Missing required environment variables: {missing_keys}")
        raise ValueError(f"Production environment missing critical secrets: {missing_keys}")
