"""Reminder service tests."""
from datetime import datetime, timedelta, timezone

import pytest

from sovereign_master.jobs.reminders import BRAND_NAME, BRANDED_SOUND_NAME, ReminderService


def test_due_reminder_is_delivered_once_with_branded_notification():
    service = ReminderService()
    due = datetime.now(timezone.utc) + timedelta(minutes=1)
    reminder = service.schedule("u1", "Call the office", due)
    events = service.poll_due(now=due + timedelta(seconds=1))

    assert events[0]["notification"]["title"] == BRAND_NAME
    assert events[0]["notification"]["sound_name"] == BRANDED_SOUND_NAME
    assert service.poll_due(now=due + timedelta(seconds=2)) == []
    assert service.list("u1") == []
    assert reminder.status == "delivered"


def test_reminder_requires_timezone_and_future_time():
    service = ReminderService()
    with pytest.raises(ValueError):
        service.schedule("u1", "No timezone", "2030-01-01T10:00:00")
