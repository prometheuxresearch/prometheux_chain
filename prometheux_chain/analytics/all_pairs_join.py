from ..client.constellation_backend_client import ConstellationBackendClient
from ..model.database import Database
import requests

def all_pairs_join(databases : list[Database], to_evaluate: bool=True, parallel: bool=False):
    try:
        response = ConstellationBackendClient.all_pairs_join(databases, to_evaluate, parallel)
        if response.status_code == 200:
           return response.json()['data']
        else:
            return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
