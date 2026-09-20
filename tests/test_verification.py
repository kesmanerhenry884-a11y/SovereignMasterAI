import unittest
from sovereign_master.verification.verifier import VerificationEngine
class VerificationTest(unittest.TestCase):
    def test_unverified(self): self.assertFalse(VerificationEngine().verify("answer", "general")["verified"])
if __name__ == "__main__": unittest.main()
