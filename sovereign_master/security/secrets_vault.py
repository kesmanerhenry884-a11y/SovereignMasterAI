"""Encrypted, explicit secrets storage; never use conversation memory for secrets."""
from cryptography.fernet import Fernet, InvalidToken
import json
import os
from threading import RLock
from typing import Any


class SecretsVault:
    def __init__(self, key: str | bytes | None = None):
        raw_key = key or os.getenv("SECRETS_MASTER_KEY", "")
        if isinstance(raw_key, str):
            raw_key = raw_key.encode()
        if not raw_key:
            raise RuntimeError("SECRETS_MASTER_KEY is required to enable the secrets vault")
        try:
            self._fernet = Fernet(raw_key)
        except (ValueError, TypeError) as exc:
            raise ValueError("SECRETS_MASTER_KEY must be a valid Fernet key") from exc
        self._items: dict[str, bytes] = {}
        self._lock = RLock()

    @staticmethod
    def generate_key() -> str:
        return Fernet.generate_key().decode()

    def set(self, user_id: str, name: str, value: str) -> None:
        if not user_id.strip() or not name.strip() or not value:
            raise ValueError("user_id, name, and value are required")
        payload = json.dumps({"user_id": user_id, "name": name, "value": value}).encode()
        with self._lock:
            self._items[f"{user_id}:{name}"] = self._fernet.encrypt(payload)

    def get(self, user_id: str, name: str) -> str | None:
        with self._lock:
            encrypted = self._items.get(f"{user_id}:{name}")
        if encrypted is None:
            return None
        try:
            return json.loads(self._fernet.decrypt(encrypted).decode())["value"]
        except (InvalidToken, KeyError, ValueError) as exc:
            raise RuntimeError("secret could not be decrypted") from exc

    def delete(self, user_id: str, name: str) -> bool:
        with self._lock:
            return self._items.pop(f"{user_id}:{name}", None) is not None

    def names(self, user_id: str) -> list[str]:
        prefix = f"{user_id}:"
        with self._lock:
            return [key[len(prefix):] for key in self._items if key.startswith(prefix)]


__all__ = ["SecretsVault"]
