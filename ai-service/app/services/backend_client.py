import logging
import random
import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import httpx
from app.config import BACKEND_BASE_URL

logger = logging.getLogger(__name__)
MAX_RETRIES = 2
MAX_RETRY_DELAY_SECONDS = 30


def _retry_delay(response: httpx.Response, attempt: int) -> float:
    """Use Retry-After when supplied, otherwise apply bounded exponential backoff."""
    retry_after = response.headers.get("Retry-After")
    if retry_after:
        try:
            delay = float(retry_after)
        except ValueError:
            try:
                retry_at = parsedate_to_datetime(retry_after)
                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=timezone.utc)
                delay = (retry_at - datetime.now(timezone.utc)).total_seconds()
            except (TypeError, ValueError, OverflowError):
                delay = 0
        if delay > 0:
            return min(delay, MAX_RETRY_DELAY_SECONDS)

    return min(2**attempt + random.uniform(0, 0.25), MAX_RETRY_DELAY_SECONDS)


def _get_json(url: str):
    for attempt in range(MAX_RETRIES + 1):
        response = httpx.get(url, timeout=10)
        if response.status_code != 429 or attempt == MAX_RETRIES:
            response.raise_for_status()
            return response.json()

        delay = _retry_delay(response, attempt)
        logger.warning(
            "Backend returned HTTP 429 for %s; retrying in %.1f seconds (%d/%d)",
            url,
            delay,
            attempt + 1,
            MAX_RETRIES,
        )
        time.sleep(delay)


def get_incident(incident_id: int):
    return _get_json(f"{BACKEND_BASE_URL}/api/incidents/{incident_id}")

def get_investigation_data(incident_id: int):
    return _get_json(
        f"{BACKEND_BASE_URL}/api/incidents/{incident_id}/investigation-data"
    )
