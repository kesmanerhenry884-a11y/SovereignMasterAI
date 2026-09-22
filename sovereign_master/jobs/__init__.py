"""Reminder scheduler boundary; production deployments can invoke poll_due periodically."""
from .reminders import REMINDER_SERVICE, Reminder, ReminderService


def poll_reminders_once():
    return REMINDER_SERVICE.poll_due()


__all__ = ["REMINDER_SERVICE", "Reminder", "ReminderService", "poll_reminders_once"]
