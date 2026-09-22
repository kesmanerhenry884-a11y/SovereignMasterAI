"""Encrypted secret vault for privileged values; not for session memory."""
from cryptography.fernet import Fernet
import json
import os
from threading import RLock


class SecretsVault:
    def __init__(self, key: str | bytes | None = None):
        raw = key or os.getenv("SECRETS_MASTER_KEY")
        if isinstance(raw, str):
            raw = raw.encode()
        if not raw:
            raise RuntimeError("SECRETS_MASTER_KEY is required")
        self._fernet = Fernet(raw)
        self._items: dict[str, bytes] = {}
        self._lock = RLock()

    @staticmethod
    def generate_key() -> str:
        return Fernet.generate_key().decode()

    def set(self, user_id: str, name: str, value: str) -> None:
        payload = json.dumps({"user_id": user_id, "name": name, "value": value}).encode()
        with self._lock:
            self._items[f"{user_id}:{name}"] = self._fernet.encrypt(payload)

    def get(self, user_id: str, name: str) -> str | None:
        with self._lock:
            encrypted = self._items.get(f"{user_id}:{name}")
        if encrypted is None:
            return None
        return json.loads(self._fernet.decrypt(encrypted).decode())["value"]

    def delete(self, user_id: str, name: str) -> bool:
        with self._lock:
            return self._items.pop(f"{user_id}:{name}", None) is not None

    def names(self, user_id: str) -> list[str]:
        prefix = f"{user_id}:"
        with self._lock:
            return [key[len(prefix):] for key in self._items if key.startswith(prefix)]


__all__ = ["SecretsVault"]
