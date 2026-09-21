from fastapi import APIRouter, HTTPException

from api.location_schemas import LocationConsentRequest, LocationResponse, PositionRequest, RouteRequest
from sovereign_master.location import LOCATION_SERVICE, Position, bearing_degrees, distance_meters

router = APIRouter(prefix="/api/v1/location", tags=["location"])


@router.post("/consent", response_model=LocationResponse)
def location_consent(request: LocationConsentRequest):
    consent = LOCATION_SERVICE.set_consent(request.user_id, request.granted, request.purpose)
    return LocationResponse(success=True, data={"user_id": consent.user_id, "granted": consent.granted, "purpose": consent.purpose, "updated_at": consent.updated_at})


@router.post("/position", response_model=LocationResponse)
def update_position(request: PositionRequest):
    try:
        position = LOCATION_SERVICE.record_position(request.user_id, Position(**request.model_dump(exclude={"user_id"})))
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail={"error": "LOCATION_CONSENT_REQUIRED", "message": str(exc)}) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return LocationResponse(success=True, data={"user_id": request.user_id, "position": position.to_dict()})


@router.get("/{user_id}", response_model=LocationResponse)
def location_status(user_id: str):
    return LocationResponse(success=True, data=LOCATION_SERVICE.status(user_id))


@router.delete("/{user_id}/position", response_model=LocationResponse)
def delete_position(user_id: str):
    deleted = LOCATION_SERVICE.delete_position(user_id)
    return LocationResponse(success=True, data={"user_id": user_id, "deleted": deleted})


@router.post("/route", response_model=LocationResponse)
def route_preview(request: RouteRequest):
    if not LOCATION_SERVICE.has_consent(request.user_id):
        raise HTTPException(status_code=403, detail={"error": "LOCATION_CONSENT_REQUIRED"})
    origin = LOCATION_SERVICE.get_position(request.user_id)
    if origin is None:
        raise HTTPException(status_code=404, detail={"error": "CURRENT_POSITION_UNAVAILABLE"})
    destination = Position(request.destination_latitude, request.destination_longitude)
    return LocationResponse(
        success=True,
        warning="This is a straight-line preview. Turn-by-turn routing requires a configured map provider.",
        data={
            "profile": request.profile,
            "origin": origin.to_dict(),
            "destination": destination.to_dict(),
            "distance_meters": round(distance_meters(origin, destination), 2),
            "initial_bearing_degrees": round(bearing_degrees(origin, destination), 2),
            "navigation_ready": False,
        },
    )
