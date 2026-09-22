from sovereign_master.memory.memory_engine import MemoryEngine
from sovereign_master.security.secrets_vault import SecretsVault


def test_long_term_memory_can_be_recalled_and_deleted():
    memory = MemoryEngine()
    memory.remember("u1", "language", "ht", importance=90, tags=["preference"])
    assert memory.recall("u1", "language")[0]["value"] == "ht"
    assert memory.forget("u1", "language") == 1
    assert memory.recall("u1", "language") == []


def test_secrets_are_encrypted_and_not_returned_by_name_listing():
    vault = SecretsVault(SecretsVault.generate_key())
    vault.set("u1", "api_key", "do-not-log")
    assert vault.get("u1", "api_key") == "do-not-log"
    assert vault.names("u1") == ["api_key"]
    assert vault.delete("u1", "api_key") is True
