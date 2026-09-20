import unittest
from sovereign_master.memory.memory_engine import MemoryEngine
class MemoryTest(unittest.TestCase):
    def test_memory(self):
        m=MemoryEngine(); m.add("s", "user", "hello"); self.assertEqual(len(m.get("s")), 1)
if __name__ == "__main__": unittest.main()
