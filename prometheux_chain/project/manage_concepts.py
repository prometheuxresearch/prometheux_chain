from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Concept Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def list_concepts(project_id, project_scope="user"):
    """
    List all concepts for a specific project.
    """
    response = JarvisPyClient.list_concepts(project_id, project_scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during listing concepts: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during listing concepts: {response.get('message', 'Unknown error')}") 
    

def overview_concepts(project_id, project_scope):
    """
    Overview the concepts of a specific project.
    """
    response = JarvisPyClient.overview_concepts(project_id, project_scope)

    print(response)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during overviewing concepts: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during overviewing concepts: {response.get('message', 'Unknown error')}")