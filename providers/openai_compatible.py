from config import CONFIG
from sovereign_master.models.provider import LocalFallbackProvider as BaseLocalFallbackProvider


class LocalFallbackProvider(BaseLocalFallbackProvider):
    name = "local_fallback"

    def generate(self, prompt: str, context: dict | None = None) -> str:
        category = (context or {}).get("category", "general")
        language = (context or {}).get("language", "auto")
        return (
            f"No real model is configured for Sovereign Master AI. "
            f"This instance is operating in safe fallback mode for category '{category}' and language '{language}'. "
            f"Set MODEL_PROVIDER, MODEL_NAME, MODEL_API_KEY and MODEL_BASE_URL in the environment to enable external generation."
        )

    def health(self):
        return {
            "provider": self.name,
            "available": True,
            "status": "fallback_active",
            "engine": CONFIG.app_name,
            "note": "This is not a live generative AI provider.",
        }
