from datetime import datetime, timezone
from typing import Any


class EventLogger:
    def __init__(self):
        self.events: list[dict[str, Any]] = []

    def record(self, event_type: str, payload: dict[str, Any] | None = None):
        event = {
            "type": event_type,
            "payload": payload or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.events.append(event)
        return event

    def recent(self, limit: int = 50) -> list[dict[str, Any]]:
        return self.events[-limit:]


OBSERVABILITY_LOGGER = EventLogger()
__all__ = ["EventLogger", "OBSERVABILITY_LOGGER"]
