from ..client.ConstellationBackendClient import ConstellationBackendClient
from ..client.JarvisClient import JarvisClient


def cleanup():
    delete_db_response = ConstellationBackendClient.delete_all_databases()
    if delete_db_response.status_code != 200:
        raise Exception(f"HTTP error! status: {delete_db_response.status_code}, detail: {delete_db_response.json()['message']}")
    print("Databases Cleanup completed")
    delete_reasoning_resource_response = JarvisClient.delete_all_resoning_resources()
    if delete_reasoning_resource_response.status_code != 200:
        raise Exception(f"HTTP error! status: {delete_reasoning_resource_response.status_code}, detail: {delete_reasoning_resource_response.json()['message']}")
    print("Reasoning Resources Cleanup completed")
