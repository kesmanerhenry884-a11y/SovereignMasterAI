import json
import os
import urllib.request

from config import CONFIG
from sovereign_master.models.provider import BaseModelProvider


class OpenAICompatibleProvider(BaseModelProvider):
    name = "openai_compatible"
    timeout_seconds = 60

    def __init__(self, api_key: str | None = None, model: str | None = None, base_url: str | None = None):
        self.api_key = api_key or os.getenv("MODEL_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.model = model or os.getenv("MODEL_NAME") or ""
        self.base_url = (base_url or os.getenv("MODEL_BASE_URL") or "https://api.openai.com/v1").rstrip("/")

    def generate(self, prompt: str, context: dict | None = None) -> str:
        if not self.api_key or not self.model:
            raise RuntimeError("MODEL_API_KEY and MODEL_NAME must be configured before using OpenAI-compatible generation")

        body = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4,
        }).encode("utf-8")

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

        choices = data.get("choices", [])
        if not choices:
            raise RuntimeError("No model output received from the configured provider")

        return choices[0].get("message", {}).get("content", "")

    def health(self):
        if not self.api_key or not self.model:
            return {
                "provider": self.name,
                "available": False,
                "status": "missing_configuration",
                "engine": CONFIG.app_name,
            }
        return {
            "provider": self.name,
            "available": True,
            "status": "configured",
            "model": self.model,
            "base_url": self.base_url,
            "engine": CONFIG.app_name,
        }
