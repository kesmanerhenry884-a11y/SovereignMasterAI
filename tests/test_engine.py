"""Final engine test suite for compatibility and core security memory invariants."""
import unittest

from sovereign_master.core.engine import SovereignMasterEngine
from sovereign_master.memory.memory_engine import MemoryEngine
from sovereign_master.security.secrets_vault import SecretsVault


class EngineTest(unittest.TestCase):
    def test_no_provider_is_explicit(self):
        result = SovereignMasterEngine().process("Bonjour")
        self.assertTrue(result["success"])
        self.assertFalse(result["verified"])

    def test_memory_remembers_and_forgets_user_fact(self):
        memory = MemoryEngine()
        memory.remember("user-1", "language", "ht", importance=90, tags=["preference"])
        recalled = memory.recall("user-1", "language")
        self.assertEqual(recalled[0]["value"], "ht")
        self.assertEqual(memory.forget("user-1", "language"), 1)

    def test_secret_vault_encrypts_and_deletes_secret(self):
        vault = SecretsVault(SecretsVault.generate_key())
        vault.set("user-1", "api_key", "supersecret")
        self.assertEqual(vault.get("user-1", "api_key"), "supersecret")
        self.assertTrue(vault.delete("user-1", "api_key"))


if __name__ == "__main__":
    unittest.main()
