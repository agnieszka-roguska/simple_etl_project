import os
import api
from dotenv import load_dotenv

from config import OPENGAGE_CONFIG
from config import DUMMYJSON_CONFIG

load_dotenv()

API_KEY = os.getenv("API_KEY")

def fetch_users_in_batches(limit: int) -> list[dict]:
    skip = 0

    while True:
        url = DUMMYJSON_CONFIG["base_url"] + DUMMYJSON_CONFIG["endpoints"]["users_url"] + f"?limit={limit}&skip={skip}"
        data = api.extract_data(url)
        users = data.get("users", [])

        if not users:
            break

        yield users

        total = data.get("total", 0)
        skip += limit

        if skip >= total:
            break


def get_country(lng: str, lat: str) -> str:
    endpoint = (
        OPENGAGE_CONFIG["base_url"] + OPENGAGE_CONFIG["endpoints"]["geocode"] + f"/json?q={lat}+{lng}&key={API_KEY}" 
    )

    data = api.extract_data(endpoint)
    try:
        return data["results"][0]["components"]["country"]
    except Exception:
        return None


def get_cart_data() -> list[dict]:
    url = DUMMYJSON_CONFIG["base_url"] + DUMMYJSON_CONFIG["endpoints"]["carts_url"]
    data = api.extract_data(url)
    return data.get("carts")
