import os
import requests
from ..config import config
import json

class VadalogClient:
    @staticmethod
    def evaluateWithParams(vadalogProgram, vadalogParams):
        VADALOG_URL = config['PMTX_URL']

        # Read the token from the environment variable if set; otherwise, use the one from config
        VADALOG_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not VADALOG_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        url = f"{VADALOG_URL}/evaluateWithParams"
        data = {
            'program': vadalogProgram,
            'params':  json.dumps(vadalogParams)
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {VADALOG_TOKEN}"
        }

        # Send the POST request with form-encoded data
        response = requests.post(url, data=data, headers=headers)

        if response.status_code != 200 and response.status_code != 504:
            raise Exception(f"Request to PMTX failed with error: {response.json()['message']}")

        return response
