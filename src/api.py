import requests

class APIRequestError(Exception):
    """Raised when an API request fails"""

def extract_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    
    except requests.exceptions.RequestException as exception:
        status = exception.response.status_code if exception.response else "unknown"
        raise APIRequestError(f"Failed to call external API. Status: {status}") from exception