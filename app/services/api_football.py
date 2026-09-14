import requests
from app.config import settings

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key" : settings.api_football_key
}

def get_from_api(endpoint:str, params: dict | None = None):
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(
        url,
        headers=HEADERS,
        params=params
    )

    response.raise_for_status()

    data = response.json()
    if data["errors"]:
        raise ValueError(
            f"API-Football error: {data['errors']}"
            )
    return data["response"]