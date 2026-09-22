"""Background reminder boundary.

Production clients should poll ``POST /api/v1/reminders/poll`` from a worker,
or replace this boundary with a durable scheduler/push provider.
"""
from .reminders import REMINDER_SERVICE, Reminder, ReminderService

__all__ = ["REMINDER_SERVICE", "Reminder", "ReminderService"]
