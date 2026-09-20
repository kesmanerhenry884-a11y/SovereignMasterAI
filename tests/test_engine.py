import unittest
from sovereign_master.core.engine import SovereignMasterEngine
class EngineTest(unittest.TestCase):
 def test_no_provider_is_explicit(self):
  result=SovereignMasterEngine().process("Bonjour")
  self.assertTrue(result["success"]); self.assertEqual(result["verified"],False)
if __name__=="__main__": unittest.main()
