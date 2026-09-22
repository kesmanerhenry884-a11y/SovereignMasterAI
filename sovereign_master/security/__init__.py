"""Compatibility and security exports."""
from sovereign_master.security.authentication import AuthGuard, TokenAuthenticator
from sovereign_master.security.permissions import PermissionManager
from sovereign_master.security.rate_limit import RateLimiter
from sovereign_master.security.secrets_vault import SecretsVault

__all__ = ["AuthGuard", "TokenAuthenticator", "PermissionManager", "RateLimiter", "SecretsVault"]
