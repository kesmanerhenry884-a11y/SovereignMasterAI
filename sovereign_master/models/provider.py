"""Provider-independent model interfaces and safe local fallback."""
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any
import json
import os

import httpx


@dataclass
class GenerationResult:
    """Normalized provider response used by modern orchestration callers."""

    text: str
    provider: str
    model: str
    metadata: dict[str, Any]


class AIProvider(ABC):
    """Modern provider contract for adapters returning GenerationResult."""

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
    """Legacy string-returning provider contract retained for compatibility."""

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
    """OpenAI-compatible chat adapter with both legacy and normalized APIs."""

    name = "openai_compatible"
    capabilities = ModelCapabilities(chat=True, streaming=True, structured_output=True)
    timeout_seconds = 120

    def __init__(self, api_key=None, model=None, base_url=None):
        self.api_key = api_key or os.getenv("AI_API_KEY") or os.getenv("MODEL_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.base_url = (base_url or os.getenv("AI_BASE_URL") or os.getenv("MODEL_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
        self.model = model or os.getenv("AI_MODEL") or os.getenv("MODEL_NAME", "")

    @staticmethod
    def _system_prompt() -> str:
        return (
            "You are the core intelligence provider of Sovereign Master AI.\n"
            "Be accurate, do not invent sources or facts, distinguish verified information "
            "from uncertainty, preserve the user's meaning, answer in the requested language "
            "when possible, and follow the application's safety policies."
        )

    def _request(self, message: str, context: dict[str, Any] | None = None, plan: list[str] | None = None) -> tuple[str, dict[str, Any]]:
        if not self.api_key or not self.model:
            raise RuntimeError("AI provider is not configured. Set AI_API_KEY and AI_MODEL.")
        messages: list[dict[str, str]] = [{"role": "system", "content": self._system_prompt()}]
        if context:
            messages.append({"role": "system", "content": "Request context:\n" + str(context)})
        messages.append({"role": "user", "content": message})
        if plan:
            messages.append({"role": "system", "content": "Execution plan:\n" + "\n".join(plan)})
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"model": self.model, "messages": messages},
            timeout=httpx.Timeout(float(self.timeout_seconds)),
        )
        response.raise_for_status()
        data = response.json()
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not text:
            raise RuntimeError("The AI provider returned an empty response.")
        return text, {"raw_id": data.get("id")}

    def generate(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        text, _ = self._request(prompt, context)
        return text

    def generate_result(self, message: str, context=None, plan=None) -> GenerationResult:
        text, metadata = self._request(message, context, plan)
        return GenerationResult(text=text, provider=self.name, model=self.model, metadata=metadata)

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
        selected = (os.getenv("AI_PROVIDER") or os.getenv("MODEL_PROVIDER") or "").strip().lower()
        if selected in {"openai", "openai_compatible"}:
            return OpenAICompatibleProvider()
        return LocalFallbackProvider()
