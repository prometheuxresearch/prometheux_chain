from ..client.ConstellationBackendClient import ConstellationBackendClient
from ..model.DbAnalytics import DbAnalytics
import requests

def all_pairs_join(db_analytics_payload : list[DbAnalytics]):

    try:
        response = ConstellationBackendClient.vadalog_db_analytics(db_analytics_payload)
        
        if response.status_code == 200:
            return response.json()['data']
        else:
            return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
    
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
