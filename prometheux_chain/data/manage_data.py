from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Data Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def cleanup_sources(workspace_id="workspace_id", source_ids=None):
    """
    Cleanup sources for a workspace.
    """
    response = JarvisPyClient.cleanup_sources(workspace_id, source_ids)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during cleaning up sources: {msg}")
    
    if response.get('status') == 'success':
        print(response.get('message', 'Project sources cleaned up successfully'))
    else:
        raise Exception(f"An exception occurred during cleaning up sources: {response.get('message', 'Unknown error')}")


def connect_sources(workspace_id="workspace_id", database_payload=None, compute_row_count=False):
    """
    Connect a source to a workspace.
    """
    response = JarvisPyClient.connect_sources(workspace_id=workspace_id, database_payload=database_payload, compute_row_count=compute_row_count)
    
    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during connecting sources: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during connecting sources: {response.get('message', 'Unknown error')}")
    

def list_sources(workspace_id="workspace_id"):
    """
    List sources for a workspace.
    """
    response = JarvisPyClient.list_sources(workspace_id=workspace_id)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during listing sources: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', [])
    else:
        raise Exception(f"An exception occurred during listing sources: {response.get('message', 'Unknown error')}")