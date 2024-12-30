# from ..client.ConstellationBackendClient import ConstellationBackendClient
# from ..model.SchemaInferencePayload import SchemaInferencePayload
# import requests
#
# def infer_from_schema(type, user, password, host, port, database, add_bind=False):
#     schema_inference_payload = SchemaInferencePayload(
#         database_type= type,
#         username=user,
#         password=password,
#         host=host,
#         port=port,
#         database= database,
#         add_bind=add_bind
#     )
#
#     try:
#         response = ConstellationBackendClient.infer_from_schema(schema_inference_payload)
#
#         if response.status_code == 200:
#             return response.json()['data']
#         else:
#             return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
#
#     except requests.exceptions.RequestException as e:
#         return f"Request failed: {e}"
