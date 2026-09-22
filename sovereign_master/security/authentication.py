"""Security primitives for authentication, permissions, rate limiting and secret handling."""
import hashlib
import hmac
import os


class TokenAuthenticator:
    def __init__(self, secret=None):
        self.secret = secret or os.getenv("ADMIN_SECRET", "")

    def issue_token(self, username):
        return hashlib.sha256(f"{username}:{self.secret}".encode()).hexdigest()

    def verify_token(self, token, username):
        return bool(self.secret and token and hmac.compare_digest(token, self.issue_token(username)))


class AuthGuard:
    def __init__(self, auth=None):
        self.auth = auth or TokenAuthenticator()

    def require_admin(self, token, username):
        return self.auth.verify_token(token, username)


class PermissionManager:
    def __init__(self, roles=None):
        self.roles = set(roles or {"user"})

    def allows(self, permission):
        return permission in self.roles or "admin" in self.roles


class RateLimiter:
    def __init__(self, limit=60, window_seconds=60):
        self.limit = int(limit)
        self.window_seconds = int(window_seconds)
        self._history = {}

    def allow(self, key: str) -> bool:
        import time
        now = time.time()
        bucket = self._history.setdefault(key, [])
        bucket[:] = [stamp for stamp in bucket if now - stamp < self.window_seconds]
        if len(bucket) >= self.limit:
            return False
        bucket.append(now)
        return True


__all__ = ["TokenAuthenticator", "AuthGuard", "PermissionManager", "RateLimiter"]
