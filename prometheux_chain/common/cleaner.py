from ..client.ConstellationBackendClient import ConstellationBackendClient

def cleanup():
    delete_db_response = ConstellationBackendClient.delete_all_databases()
    if delete_db_response.status_code != 200:
        raise Exception(f"HTTP error! status: {delete_db_response.status_code}, detail: {delete_db_response.json()['message']}")
    print("Cleanup completed")
