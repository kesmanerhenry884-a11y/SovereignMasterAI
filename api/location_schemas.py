from typing import Any

from pydantic import BaseModel, Field


class LocationConsentRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=200)
    granted: bool
    purpose: str = Field(min_length=1, max_length=500)


class PositionRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=200)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    accuracy_meters: float | None = Field(default=None, ge=0)
    heading: float | None = Field(default=None, ge=0, le=360)
    speed_mps: float | None = Field(default=None, ge=0)
    captured_at: str | None = None


class RouteRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=200)
    destination_latitude: float = Field(ge=-90, le=90)
    destination_longitude: float = Field(ge=-180, le=180)
    profile: str = Field(default="walking", max_length=30)


class LocationResponse(BaseModel):
    success: bool
    data: dict[str, Any] = Field(default_factory=dict)
    warning: str | None = None
