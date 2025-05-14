from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Data Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def cleanup_sources(project_id, project_scope="user", source_ids=None):
    """
    Cleanup kg sources for a project.
    """
    response = JarvisPyClient.cleanup_sources(project_id, project_scope, source_ids)

    print(response)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during cleaning up kg sources: {msg}")
    
    if response.get('status') == 'success':
        print(response.get('message', 'Project sources cleaned up successfully'))
    else:
        raise Exception(f"An exception occurred during cleaning up kg sources: {response.get('message', 'Unknown error')}")


def connect_sources(project_id, project_scope, database_payload, add_model=False):
    response = JarvisPyClient.connect_sources(project_id, project_scope, database_payload, add_model)
    
    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during connecting sources: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during connecting sources: {response.get('message', 'Unknown error')}")
    

def list_sources(project_id, project_scope):
    response = JarvisPyClient.list_sources(project_id, project_scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during listing sources: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during listing sources: {response.get('message', 'Unknown error')}")