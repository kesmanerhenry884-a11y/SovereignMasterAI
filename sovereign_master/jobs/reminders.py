"""Reminder scheduling and branded notification events.

The service is deliberately transport-independent: API clients can turn a due
notification into a push notification, message, or device alarm. The engine
never pretends it can ring a phone without a connected client.
"""
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from threading import RLock
from typing import Any
from uuid import uuid4


BRAND_NAME = "PROPHÈTE KESMANER HENRY"
BRANDED_SOUND_NAME = "prophete_kesmaner_henry_reminder"


def _parse_time(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        moment = value
    else:
        normalized = value.strip().replace("Z", "+00:00")
        moment = datetime.fromisoformat(normalized)
    if moment.tzinfo is None:
        raise ValueError("reminder time must include a timezone offset")
    return moment.astimezone(timezone.utc)


@dataclass
class Reminder:
    id: str
    user_id: str
    message: str
    due_at: str
    status: str = "scheduled"
    notify: bool = True
    sound: bool = True
    created_at: str = ""
    delivered_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self) | {
            "title": BRAND_NAME,
            "sound_name": BRANDED_SOUND_NAME if self.sound else None,
        }


class ReminderService:
    """Create, remember and deliver reminders once when they become due."""

    def __init__(self):
        self._reminders: dict[str, Reminder] = {}
        self._lock = RLock()

    def schedule(
        self,
        user_id: str,
        message: str,
        due_at: str | datetime,
        *,
        notify: bool = True,
        sound: bool = True,
    ) -> Reminder:
        if not user_id.strip() or not message.strip():
            raise ValueError("user_id and message are required")
        moment = _parse_time(due_at)
        if moment <= datetime.now(timezone.utc):
            raise ValueError("reminder time must be in the future")
        now = datetime.now(timezone.utc).isoformat()
        reminder = Reminder(
            id=str(uuid4()),
            user_id=user_id.strip(),
            message=message.strip(),
            due_at=moment.isoformat(),
            notify=notify,
            sound=sound,
            created_at=now,
        )
        with self._lock:
            self._reminders[reminder.id] = reminder
        return reminder

    def list(self, user_id: str, *, include_delivered: bool = False) -> list[dict[str, Any]]:
        with self._lock:
            reminders = [
                reminder for reminder in self._reminders.values()
                if reminder.user_id == user_id and (include_delivered or reminder.status != "delivered")
            ]
        reminders.sort(key=lambda reminder: reminder.due_at)
        return [reminder.to_dict() for reminder in reminders]

    def cancel(self, user_id: str, reminder_id: str) -> bool:
        with self._lock:
            reminder = self._reminders.get(reminder_id)
            if reminder is None or reminder.user_id != user_id or reminder.status == "delivered":
                return False
            reminder.status = "cancelled"
            return True

    def poll_due(self, *, now: datetime | None = None) -> list[dict[str, Any]]:
        current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
        due: list[dict[str, Any]] = []
        with self._lock:
            for reminder in self._reminders.values():
                if reminder.status != "scheduled" or _parse_time(reminder.due_at) > current:
                    continue
                reminder.status = "delivered"
                reminder.delivered_at = current.isoformat()
                if reminder.notify:
                    due.append({
                        "event": "reminder.due",
                        "reminder": reminder.to_dict(),
                        "notification": {
                            "title": BRAND_NAME,
                            "body": reminder.message,
                            "sound": reminder.sound,
                            "sound_name": BRANDED_SOUND_NAME if reminder.sound else None,
                            "requires_client_delivery": True,
                        },
                    })
        return due


REMINDER_SERVICE = ReminderService()

__all__ = ["Reminder", "ReminderService", "REMINDER_SERVICE", "BRAND_NAME", "BRANDED_SOUND_NAME"]
