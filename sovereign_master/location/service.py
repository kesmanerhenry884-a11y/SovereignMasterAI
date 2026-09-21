from dataclasses import dataclass
from datetime import datetime, timezone
from math import atan2, cos, radians, sin, sqrt
from threading import RLock
from typing import Any
from uuid import uuid4


@dataclass
class LocationConsent:
    user_id: str
    granted: bool
    purpose: str
    updated_at: str


@dataclass
class Position:
    latitude: float
    longitude: float
    accuracy_meters: float | None = None
    heading: float | None = None
    speed_mps: float | None = None
    captured_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "accuracy_meters": self.accuracy_meters,
            "heading": self.heading,
            "speed_mps": self.speed_mps,
            "captured_at": self.captured_at,
        }


class LocationService:
    """Consent-first location boundary; the client supplies GPS coordinates."""

    def __init__(self):
        self._consents: dict[str, LocationConsent] = {}
        self._positions: dict[str, Position] = {}
        self._lock = RLock()

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def validate_position(position: Position) -> None:
        if not -90 <= position.latitude <= 90:
            raise ValueError("latitude must be between -90 and 90")
        if not -180 <= position.longitude <= 180:
            raise ValueError("longitude must be between -180 and 180")
        if position.accuracy_meters is not None and position.accuracy_meters < 0:
            raise ValueError("accuracy_meters cannot be negative")

    def set_consent(self, user_id: str, granted: bool, purpose: str) -> LocationConsent:
        if not user_id.strip() or not purpose.strip():
            raise ValueError("user_id and purpose are required")
        consent = LocationConsent(user_id, granted, purpose, self._now())
        with self._lock:
            self._consents[user_id] = consent
            if not granted:
                self._positions.pop(user_id, None)
        return consent

    def has_consent(self, user_id: str) -> bool:
        with self._lock:
            return bool(self._consents.get(user_id, None) and self._consents[user_id].granted)

    def record_position(self, user_id: str, position: Position) -> Position:
        if not self.has_consent(user_id):
            raise PermissionError("location consent is required")
        self.validate_position(position)
        if position.captured_at is None:
            position.captured_at = self._now()
        with self._lock:
            self._positions[user_id] = position
        return position

    def get_position(self, user_id: str) -> Position | None:
        if not self.has_consent(user_id):
            return None
        with self._lock:
            return self._positions.get(user_id)

    def delete_position(self, user_id: str) -> bool:
        with self._lock:
            return self._positions.pop(user_id, None) is not None

    def status(self, user_id: str) -> dict[str, Any]:
        consent = self._consents.get(user_id)
        position = self.get_position(user_id)
        return {
            "user_id": user_id,
            "consent_granted": bool(consent and consent.granted),
            "consent_purpose": consent.purpose if consent else None,
            "position": position.to_dict() if position else None,
        }


def distance_meters(start: Position, end: Position) -> float:
    earth_radius = 6_371_000
    lat_delta = radians(end.latitude - start.latitude)
    lon_delta = radians(end.longitude - start.longitude)
    a = sin(lat_delta / 2) ** 2 + cos(radians(start.latitude)) * cos(radians(end.latitude)) * sin(lon_delta / 2) ** 2
    return earth_radius * 2 * atan2(sqrt(a), sqrt(1 - a))


def bearing_degrees(start: Position, end: Position) -> float:
    lat1, lat2 = radians(start.latitude), radians(end.latitude)
    delta_lon = radians(end.longitude - start.longitude)
    value = atan2(sin(delta_lon) * cos(lat2), cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(delta_lon))
    return (value * 180 / 3.141592653589793 + 360) % 360


LOCATION_SERVICE = LocationService()
