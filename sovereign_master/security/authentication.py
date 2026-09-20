import hmac, os
class Authenticator:
    def verify(self, provided): return bool(provided and hmac.compare_digest(provided, os.getenv("ADMIN_SECRET", "")))
