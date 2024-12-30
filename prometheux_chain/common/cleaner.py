from ..client.JarvisPyClient import JarvisPyClient


def cleanup(kg_path=None):
    """
    Cleanup all virtual kg resources for the user with optional kg_path.
    """
    delete_virtual_kg_resource_response = JarvisPyClient.delete_all_virtual_kg_resources()
    if delete_virtual_kg_resource_response.status_code != 200:
        raise Exception(f"HTTP error! status: {delete_virtual_kg_resource_response.status_code}, "
                        f"detail: {delete_virtual_kg_resource_response.json()['message']}")
    print("Virtual Knowledge Graph Resources Cleanup completed")
