from ..client.constellation_backend_client import ConstellationBackendClient
from ..model.database import Database
import requests

def infer_schema(database:Database, add_bind=True, add_model=False):
    try:
        response = ConstellationBackendClient.infer_schema(database, add_bind, add_model)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"