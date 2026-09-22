"""Final compatibility contract tests."""
from sovereign_master.models.normalize import normalize_generation_result


class FakeProvider:
    name = "test"
    model = "test-model"

    def generate(self, message, context=None, plan=None):
        return "legacy response"


def test_generation_result_contract_is_preserved():
    provider = FakeProvider()
    normalized = normalize_generation_result(provider.generate("hello"), provider)
    assert normalized.text == "legacy response"
    assert normalized.provider == "test"
    assert normalized.model == "test-model"
    assert normalized.metadata["legacy_adapter"] is True
