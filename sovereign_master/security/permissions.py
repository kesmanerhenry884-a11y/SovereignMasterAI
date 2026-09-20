class PermissionManager:
    def __init__(self, roles=None): self.roles=set(roles or {"user"})
    def allows(self, permission): return permission in self.roles or "admin" in self.roles
