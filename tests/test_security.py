import unittest
from sovereign_master.security.authentication import TokenAuthenticator
class AuthTest(unittest.TestCase):
 def test_admin_token(self):
  auth=TokenAuthenticator("secret"); token=auth.issue_token("admin"); self.assertTrue(auth.verify_token(token,"admin")); self.assertFalse(auth.verify_token(token,"other"))
if __name__=="__main__": unittest.main()
