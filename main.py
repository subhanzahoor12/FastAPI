from fastapi import FastAPI,Body
from sqlmodel import SQLModel
from fastapi_practice.cores.database import engine
from fastapi_practice.routers import authentication, blog, user
from eventbrite_api import create_event, get_events
from fastapi_practice.cores.models import EventData

app = FastAPI()

# models.Base.metadata.drop_all(engine)
SQLModel.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)

@app.post("/eventbrite/create-event/{organization_id}")
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


@app.get("/eventbrite/events/{organization_id}")
async def get_event_endpoint(organization_id: str):
    result = await get_events(organization_id)
    return result