import unittest
from database.connection import DatabaseAdapter
from database.repository import MemoryRepository
class PersistenceTest(unittest.TestCase):
 def test_sqlite_memory(self):
  repo=MemoryRepository(DatabaseAdapter()); repo.add_message("s","user","hello"); self.assertEqual(repo.get_messages("s")[0]["content"],"hello")
if __name__=="__main__": unittest.main()
