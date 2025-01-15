from ..client.JarvisPyClient import JarvisPyClient

"""
Resource Cleanup Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def cleanup(virtual_kg=None):
    """
    Cleanup Virtual KG resources for the user.
    If `virtual_kg` is provided, it only cleans up resources for that KG.
    If `virtual_kg` is None, it cleans up all resources for the user associated with the PMTX token.
    """
    if virtual_kg is not None:
        delete_virtual_kg_resource_response = JarvisPyClient.delete_virtual_kg_resources(virtual_kg)
    else:
        delete_virtual_kg_resource_response = JarvisPyClient.delete_virtual_kg_resources()

    if delete_virtual_kg_resource_response.status_code != 200:
        json_resp = delete_virtual_kg_resource_response.json()
        msg = json_resp.get('message', 'Unknown error')
        raise Exception(f"HTTP error! status: {delete_virtual_kg_resource_response.status_code}, detail: {msg}")

    if virtual_kg is not None:
        print(f"Cleanup of virtual knowledge graph ID={virtual_kg.get('id')} "
              f"for the user associated with the PMTX token completed successfully")
    else:
        print("Cleanup of all resources for the user associated with the PMTX token completed successfully")

