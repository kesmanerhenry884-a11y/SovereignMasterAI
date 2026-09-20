import unittest
from sovereign_master.core.task_router import TaskRouter
class RouterTest(unittest.TestCase):
    def test_math(self): self.assertEqual(TaskRouter().classify("calculate 2 + 2"), "math")
if __name__ == "__main__": unittest.main()
