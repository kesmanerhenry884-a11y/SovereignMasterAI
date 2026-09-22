"""Provider-independent model interfaces and safe local fallback."""
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any
import json
import os
import urllib.request


@dataclass
class GenerationResult:
    """Normalized provider response used by modern orchestration callers."""

    text: str
    provider: str
    model: str
    metadata: dict[str, Any]


class AIProvider(ABC):
    """Modern provider contract; legacy providers remain supported separately."""

    name: str = "unknown"

    @abstractmethod
    def generate(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        plan: list[str] | None = None,
    ) -> GenerationResult:
        raise NotImplementedError


@dataclass(frozen=True)
class ModelCapabilities:
    chat: bool = True
    streaming: bool = False
    vision: bool = False
    tools: bool = False
    structured_output: bool = False


class BaseModelProvider(ABC):
    """Legacy provider contract retained for existing adapters."""

    name = "base"
    model = ""
    capabilities = ModelCapabilities()
    timeout_seconds = 30

    @abstractmethod
    def generate(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        raise NotImplementedError

    def stream(self, prompt, context=None):
        yield self.generate(prompt, context)

    def health(self):
        return {
            "provider": self.name,
            "available": False,
            "status": "not_configured",
            "capabilities": asdict(self.capabilities),
        }

    def metadata(self):
        return {
            "name": self.name,
            "model": self.model,
            "timeout_seconds": self.timeout_seconds,
            "capabilities": asdict(self.capabilities),
        }

    def generate_result(
        self,
        message: str,
        context: dict[str, Any] | None = None,
        plan: list[str] | None = None,
    ) -> GenerationResult:
        """Adapt an existing string provider to the normalized result contract."""
        text = self.generate(message, {**(context or {}), "plan": plan or []})
        return GenerationResult(
            text=text,
            provider=self.name,
            model=getattr(self, "model", ""),
            metadata={"legacy_adapter": True},
        )


class LocalFallbackProvider(BaseModelProvider):
    name = "local_fallback"
    capabilities = ModelCapabilities(chat=False)

    def generate(self, prompt, context=None):
        raise RuntimeError("No generative model is configured")

    def health(self):
        return {
            **super().health(),
            "status": "fallback_only",
            "note": "Not a generative AI model",
        }


class OpenAICompatibleProvider(BaseModelProvider):
    """Adapter for any OpenAI-compatible HTTP API; credentials stay in env vars."""

    name = "openai_compatible"
    capabilities = ModelCapabilities(chat=True, streaming=True, structured_output=True)
    timeout_seconds = 60

    def __init__(self, api_key=None, model=None, base_url=None):
        self.api_key = api_key or os.getenv("MODEL_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("MODEL_NAME", "")
        self.base_url = (base_url or os.getenv("MODEL_BASE_URL", "https://api.openai.com/v1")).rstrip("/")

    def _request(self, prompt):
        if not self.api_key or not self.model:
            raise RuntimeError("MODEL_API_KEY and MODEL_NAME are required")
        body = json.dumps({"model": self.model, "messages": [{"role": "user", "content": prompt}]}).encode()
        req = urllib.request.Request(
            self.base_url + "/chat/completions",
            body,
            {"Content-Type": "application/json", "Authorization": "Bearer " + self.api_key},
        )
        with urllib.request.urlopen(req, timeout=self.timeout_seconds) as response:
            data = json.loads(response.read().decode())
        return data["choices"][0]["message"]["content"]

    def generate(self, prompt, context=None):
        return self._request(prompt)

    def health(self):
        configured = bool(self.api_key and self.model)
        return {
            **super().health(),
            "available": configured,
            "status": "configured" if configured else "missing_configuration",
            "model": self.model,
        }


class ProviderFactory:
    @staticmethod
    def create_from_environment():
        selected = os.getenv("MODEL_PROVIDER", "").strip().lower()
        if selected in {"openai", "openai_compatible"}:
            return OpenAICompatibleProvider()
        return LocalFallbackProvider()
