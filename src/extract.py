import os

import requests

import transform

API_KEY = os.getenv("API_KEY")


def fetch_users_in_batches(base_url: str, limit: int) -> list[dict]:
    all_users = list()
    skip = 0
    while True:
        url = base_url + f"?limit={limit}&skip={skip}"
        response = requests.get(url)
        data = response.json()
        users = data.get("users")
        if not users:  # break loop when 'users' is empty
            break
        users_processed = transform.process_users_data(users)
        all_users += users_processed
        total = data.get("total", 0)

        if skip + limit >= total:
            break
        skip += limit

    return all_users


def get_country(lng: str, lat: str) -> str:
    endpoint = (
        f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lng}&key={API_KEY}"
    )
    response = requests.get(endpoint)
    data = response.json()
    try:
        return data["results"][0]["components"]["country"]
    except Exception:
        return "Unknown"


def get_cart_data() -> list[dict]:
    url = "https://dummyjson.com/carts"
    response = requests.get(url)
    data = response.json()
    return data.get("carts")
