import hmac, hashlib, os
class TokenAuthenticator:
    def __init__(self, secret=None): self.secret=secret or os.getenv("ADMIN_SECRET","")
    def issue_token(self, username): return hashlib.sha256(f"{username}:{self.secret}".encode()).hexdigest()
    def verify_token(self, token, username): return bool(self.secret and token and hmac.compare_digest(token,self.issue_token(username)))
class AuthGuard:
    def __init__(self, auth=None): self.auth=auth or TokenAuthenticator()
    def require_admin(self, token, username): return self.auth.verify_token(token,username)
