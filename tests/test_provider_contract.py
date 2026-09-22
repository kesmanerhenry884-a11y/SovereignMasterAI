from dataclasses import dataclass
from typing import Any

from sovereign_master.models.provider import GenerationResult
from sovereign_master.models.normalize import normalize_generation_result


@dataclass
class FakeProvider:
    name: str = "test"
    model: str = "test-model"

    def generate(self, message: str, context: dict[str, Any] | None = None, plan=None):
        return GenerationResult(
            text="generated",
            provider=self.name,
            model=self.model,
            metadata={"plan": plan or []},
        )


def test_generation_result_contract_is_preserved():
    provider = FakeProvider()
    result = normalize_generation_result(provider.generate("hello", plan=["respond"]), provider)

    assert result.text == "generated"
    assert result.provider == "test"
    assert result.model == "test-model"
    assert result.metadata["plan"] == ["respond"]


def test_legacy_string_result_is_normalized():
    provider = FakeProvider()
    result = normalize_generation_result("legacy response", provider)

    assert result.text == "legacy response"
    assert result.metadata["legacy_adapter"] is True
