import httpx

from fastapi_practice.cores.config import EVENTBRITE_TOKEN, EVENTBRITE_URL

EVENTBRITE_API = EVENTBRITE_URL
TOKEN = EVENTBRITE_TOKEN
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}


async def create_event(organization_id: str, event_data: dict):
    url = f"{EVENTBRITE_API}/organizations/{organization_id}/events/"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=HEADERS, json=event_data)
        return response.json()


async def get_events(organization_id: str):
    url = f"{EVENTBRITE_API}/organizations/{organization_id}/events/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        return response.json()
