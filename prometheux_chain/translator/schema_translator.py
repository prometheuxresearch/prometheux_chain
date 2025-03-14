from ..client.constellation_backend_client import ConstellationBackendClient
from ..model.schema_inference_payload import SchemaInferencePayload
import requests

def infer_from_schema(type, user, password, host, port, database, table=None, query=None, add_bind=False, options=None):
    if options is None:
        options = {}
    
    schema_inference_payload = SchemaInferencePayload(
        database_type=type,
        username=user,
        password=password,
        host=host,
        port=port,
        database=database,
        table=table,
        query=query,
        add_bind=add_bind,
        options=options,
    )
    try:
        response = ConstellationBackendClient.infer_from_schema(schema_inference_payload)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"