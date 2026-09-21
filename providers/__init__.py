import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from typing import Any
import json
import urllib.request


@dataclass(frozen=True)
class ModelCapabilities:
    chat: bool = True
    streaming: bool = False
    vision: bool = False
    tools: bool = False
    structured_output: bool = False


class BaseModelProvider(ABC):
    name = "base"
    capabilities = ModelCapabilities()
    timeout_seconds = 30

    def metadata(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "timeout_seconds": self.timeout_seconds,
            "capabilities": asdict(self.capabilities),
        }

    @abstractmethod
    def generate(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        raise NotImplementedError

    def stream(self, prompt: str, context: dict[str, Any] | None = None):
        yield self.generate(prompt, context)

    def health(self) -> dict[str, Any]:
        return {"provider": self.name, "available": False, "status": "not_configured"}


class LocalFallbackProvider(BaseModelProvider):
    name = "local_fallback"
    capabilities = ModelCapabilities(chat=True, structured_output=True)

    def generate(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        category = (context or {}).get("category", "general")
        mode = (context or {}).get("mode", "general")
        language = (context or {}).get("language", "auto")
        return (
            f"No generative model is configured in this environment. "
            f"The request was classified under '{category}' in '{language}' mode. "
            f"The engine is ready for a real provider, but it is not pretending to have a live AI model yet."
        )

    def health(self) -> dict[str, Any]:
        return {
            "provider": self.name,
            "available": True,
            "status": "fallback_active",
            "note": "This is a safe local fallback, not a real external AI model.",
        }


class OpenAICompatibleProvider(BaseModelProvider):
    name = "openai_compatible"
    capabilities = ModelCapabilities(chat=True, streaming=True, structured_output=True)
    timeout_seconds = 60

    def __init__(self, api_key: str | None = None, model: str | None = None, base_url: str | None = None):
        self.api_key = api_key or os.getenv("MODEL_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("MODEL_NAME", "")
        self.base_url = (base_url or os.getenv("MODEL_BASE_URL", "https://api.openai.com/v1")).rstrip("/")

    def generate(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        if not self.api_key or not self.model:
            raise RuntimeError("MODEL_API_KEY and MODEL_NAME must be set for OpenAI-compatible generation")

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
        }
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=self.timeout_seconds) as response:
            data = json.loads(response.read().decode("utf-8"))

        if not data.get("choices"):
            raise RuntimeError("Model provider returned no choices")

        content = data["choices"][0]["message"].get("content", "")
        return content if isinstance(content, str) else str(content)

    def health(self) -> dict[str, Any]:
        if not self.api_key or not self.model:
            return {
                "provider": self.name,
                "available": False,
                "status": "missing_configuration",
                "reason": "Set MODEL_API_KEY and MODEL_NAME",
            }
        return {
            "provider": self.name,
            "available": True,
            "status": "configured",
            "model": self.model,
            "base_url": self.base_url,
        }


class ProviderFactory:
    @staticmethod
    def build() -> BaseModelProvider:
        provider_name = os.getenv("MODEL_PROVIDER", "local_fallback").strip().lower()
        if provider_name in {"openai", "openai_compatible"}:
            return OpenAICompatibleProvider()
        return LocalFallbackProvider()
