from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from threading import RLock
from uuid import uuid4

BRAND_NAME = "PROPHÈTE KESMANER HENRY"
BRANDED_SOUND_NAME = "prophete_kesmaner_henry_reminder"


def _parse_time(value):
    moment = value if isinstance(value, datetime) else datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    if moment.tzinfo is None: raise ValueError("reminder time must include a timezone offset")
    return moment.astimezone(timezone.utc)

@dataclass
class Reminder:
    id: str; user_id: str; message: str; due_at: str; status: str = "scheduled"; notify: bool = True; sound: bool = True; created_at: str = ""; delivered_at: str | None = None
    def to_dict(self): return asdict(self) | {"title": BRAND_NAME, "sound_name": BRANDED_SOUND_NAME if self.sound else None}

class ReminderService:
    def __init__(self, repository=None):
        self.repository = repository; self._reminders = {}; self._lock = RLock()
        if repository and hasattr(repository, "get_reminders"):
            for item in repository.get_reminders("__bootstrap_never__", include_delivered=True): self._reminders[item["id"]] = Reminder(**item)

    def schedule(self, user_id, message, due_at, *, notify=True, sound=True):
        moment = _parse_time(due_at)
        if not user_id.strip() or not message.strip(): raise ValueError("user_id and message are required")
        if moment <= datetime.now(timezone.utc): raise ValueError("reminder time must be in the future")
        reminder = Reminder(str(uuid4()), user_id.strip(), message.strip(), moment.isoformat(), notify=notify, sound=sound, created_at=datetime.now(timezone.utc).isoformat())
        with self._lock: self._reminders[reminder.id] = reminder
        if self.repository and hasattr(self.repository, "save_reminder"): self.repository.save_reminder(reminder)
        return reminder

    def list(self, user_id, *, include_delivered=False):
        items = [r for r in self._reminders.values() if r.user_id == user_id and (include_delivered or r.status not in {"delivered", "cancelled"})]
        if self.repository and hasattr(self.repository, "get_reminders"):
            persisted = {r["id"]: r for r in self.repository.get_reminders(user_id, include_delivered)}
            for item in persisted.values(): self._reminders[item["id"]] = Reminder(**item)
            items = [r for r in self._reminders.values() if r.user_id == user_id and (include_delivered or r.status not in {"delivered", "cancelled"})]
        return [r.to_dict() for r in sorted(items, key=lambda r: r.due_at)]

    def cancel(self, user_id, reminder_id):
        with self._lock:
            reminder = self._reminders.get(reminder_id)
            if not reminder and self.repository and hasattr(self.repository, "get_reminders"):
                matches = [r for r in self.repository.get_reminders(user_id, True) if r["id"] == reminder_id]
                reminder = Reminder(**matches[0]) if matches else None
                if reminder: self._reminders[reminder.id] = reminder
            if not reminder or reminder.user_id != user_id or reminder.status in {"delivered", "cancelled"}: return False
            reminder.status = "cancelled"
            if self.repository and hasattr(self.repository, "save_reminder"): self.repository.save_reminder(reminder)
            return True

    def poll_due(self, *, now=None):
        current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc); events = []
        for reminder in list(self._reminders.values()):
            if reminder.status != "scheduled" or _parse_time(reminder.due_at) > current: continue
            reminder.status = "delivered"; reminder.delivered_at = current.isoformat()
            if self.repository and hasattr(self.repository, "save_reminder"): self.repository.save_reminder(reminder)
            if reminder.notify: events.append({"event": "reminder.due", "reminder": reminder.to_dict(), "notification": {"title": BRAND_NAME, "body": reminder.message, "sound": reminder.sound, "sound_name": BRANDED_SOUND_NAME if reminder.sound else None, "requires_client_delivery": True}})
        return events

REMINDER_SERVICE = ReminderService()
