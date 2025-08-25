from fastapi import APIRouter, Body

from fastapi_practice.cores.models import EventData
from fastapi_practice.repository.eventbrite_api import create_event, get_events

router = APIRouter(prefix="/eventbrite", tags=["EventBrite"])


@router.post("/create-event/{organization_id}")
async def create_event_endpoint(
    organization_id: str, data: EventData = Body(...)
):
    event_payload = {
        "event": {
            "name": {"html": data.name},
            "start": {"utc": data.start, "timezone": "UTC"},
            "end": {"utc": data.end, "timezone": "UTC"},
            "currency": data.currency,
        }
    }
    result = await create_event(organization_id, event_payload)
    return result


@router.get("/events/{organization_id}")
async def get_event_endpoint(organization_id: str):
    result = await get_events(organization_id)
    return result
