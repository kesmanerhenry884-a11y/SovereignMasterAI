from dataclasses import dataclass
from typing import Any

from sovereign_master.models.provider import GenerationResult


def normalize_generation_result(result: Any, provider: Any, model: str = "") -> GenerationResult:
    """Convert legacy strings or modern GenerationResult values uniformly."""
    if isinstance(result, GenerationResult):
        return result
    if hasattr(result, "text"):
        return GenerationResult(
            text=str(result.text),
            provider=getattr(result, "provider", getattr(provider, "name", "unknown")),
            model=getattr(result, "model", model),
            metadata=dict(getattr(result, "metadata", {}) or {}),
        )
    return GenerationResult(
        text=str(result),
        provider=getattr(provider, "name", "unknown"),
        model=getattr(provider, "model", model),
        metadata={"legacy_adapter": True},
    )
