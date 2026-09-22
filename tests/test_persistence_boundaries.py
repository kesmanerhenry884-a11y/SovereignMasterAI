from datetime import datetime, timezone
from sovereign_master.jobs.reminders import ReminderService


def test_durable_memory_and_reminders_are_available():
    assert hasattr(ReminderService(), "poll_due")
