import requests
import json
from ..config import config
from ..model.SchemaInferencePayload import SchemaInferencePayload

class ConstellationBackendClient:

    @staticmethod
    def infer_from_schema(schema_inference_payload: SchemaInferencePayload):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(schema_inference_payload.to_dict())
        
        try:
            response = requests.post(
                f"{config['CONSTELLATION_BACKEND_URL']}/schema-info/inferFromSchema",
                headers=headers,
                data=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {e}"}
