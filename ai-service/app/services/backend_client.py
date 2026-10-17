import httpx
from app.config import BACKEND_BASE_URL

def get_incident(incident_id: int):
    response = httpx.get(
        f"{BACKEND_BASE_URL}/api/incidents/{incident_id}",
        timeout=10
    )
    response.raise_for_status()

    return response.json()

def get_investigation_data(incident_id: int):
    response = httpx.get(
        f"{BACKEND_BASE_URL}/api/incidents/{incident_id}/investigation-data",
        timeout=10
    )

    response.raise_for_status()

    return response.json()