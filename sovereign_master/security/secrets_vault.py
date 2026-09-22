"""Encrypted secrets vault with optional encrypted persistence."""
from cryptography.fernet import Fernet
import json
import os
from threading import RLock


class SecretsVault:
    def __init__(self, key=None, repository=None):
        raw = key or os.getenv("SECRETS_MASTER_KEY")
        if isinstance(raw, str):
            raw = raw.encode()
        if not raw:
            raise RuntimeError("SECRETS_MASTER_KEY is required")
        self._fernet = Fernet(raw)
        self.repository = repository
        self._items = {}
        self._lock = RLock()

    @staticmethod
    def generate_key():
        return Fernet.generate_key().decode()

    def set(self, user_id, name, value):
        if not user_id.strip() or not name.strip() or not value:
            raise ValueError("user_id, name, and value are required")
        encrypted = self._fernet.encrypt(json.dumps({"user_id": user_id, "name": name, "value": value}).encode())
        with self._lock:
            self._items[f"{user_id}:{name}"] = encrypted
        if self.repository and hasattr(self.repository, "set_secret"):
            self.repository.set_secret(user_id, name, encrypted)

    def get(self, user_id, name):
        with self._lock:
            encrypted = self._items.get(f"{user_id}:{name}")
        if encrypted is None and self.repository and hasattr(self.repository, "get_secret"):
            encrypted = self.repository.get_secret(user_id, name)
        if encrypted is None:
            return None
        return json.loads(self._fernet.decrypt(encrypted).decode())["value"]

    def delete(self, user_id, name):
        with self._lock:
            removed = self._items.pop(f"{user_id}:{name}", None) is not None
        if self.repository and hasattr(self.repository, "delete_secret"):
            removed = self.repository.delete_secret(user_id, name) or removed
        return removed

    def names(self, user_id):
        prefix = f"{user_id}:"
        with self._lock:
            return sorted([key[len(prefix):] for key in self._items if key.startswith(prefix)])


__all__ = ["SecretsVault"]
