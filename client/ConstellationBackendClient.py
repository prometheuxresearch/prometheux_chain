import requests
import json
from ..config import config

class ConstellationBackendClient:
    @staticmethod
    def store_database_info(database_info):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(database_info.to_dict())

        response = requests.post(f"{config['CONSTELLATION_BACKEND_URL']}/database-info/store", headers=headers, data=data)

        if response.status_code != 200:
            raise Exception(f"HTTP error! status: {response.status_code}, detail: {response.text}")

        json_response = response.json()
        if 'data' in json_response:
            return json_response['data']
        else:
            return None
