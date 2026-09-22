from dataclasses import dataclass
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from sovereign_master.jobs.reminders import REMINDER_SERVICE

router = APIRouter(prefix="/api/v1/reminders", tags=["reminders"])


class ReminderRequest(BaseModel):
    user_id: str = Field(min_length=1)
    message: str = Field(min_length=1)
    due_at: str
    notify: bool = True
    sound: bool = True


@router.post("")
def create_reminder(request: ReminderRequest):
    try:
        reminder = REMINDER_SERVICE.schedule(
            request.user_id,
            request.message,
            request.due_at,
            notify=request.notify,
            sound=request.sound,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"success": True, "reminder": reminder.to_dict()}


@router.get("")
def list_reminders(user_id: str, include_delivered: bool = False):
    return {"reminders": REMINDER_SERVICE.list(user_id, include_delivered=include_delivered)}


@router.post("/poll")
def poll_reminders():
    return {"events": REMINDER_SERVICE.poll_due()}


@router.delete("/{reminder_id}")
def cancel_reminder(reminder_id: str, user_id: str):
    if not REMINDER_SERVICE.cancel(user_id, reminder_id):
        raise HTTPException(status_code=404, detail="Reminder not found or already delivered")
    return {"success": True, "reminder_id": reminder_id, "status": "cancelled"}
