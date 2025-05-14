from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Project Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def cleanup_projects(project_id=None, project_scope="user"):
    """
    Cleanup project resources for the user.
    If `project_id` is provided, it only cleans up resources for that project.
    If `project_id` is None, it cleans up all project resources for the user associated with the PMTX token.
    """
    response = JarvisPyClient.cleanup_projects(project_id=project_id, project_scope=project_scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during cleaning up project: {msg}")
    
    if response.get('status') == 'success':
        print(response.get('message', 'Project resources cleaned up successfully'))
    else:
        raise Exception(f"An exception occurred during cleaning up project: {response.get('message', 'Unknown error')}") 
    

def save_project(project_id=None, project_scope="user", to_persist=True):
    """
    Save a project.
    """
    response = JarvisPyClient.save_project(project_id=project_id, project_scope=project_scope, to_persist=to_persist)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while saving project: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {}).get('project_id')
    else:
        raise Exception(f"An exception occurred while saving project: {response.get('message', 'Unknown error')}")


def list_projects(scopes=["user"]):
    """
    List all projects saved by the user.
    """
    projects_ids = []
    for scope in scopes:
        response = JarvisPyClient.list_projects(scope=scope)

        if response.get('status') != 'success':
            msg = response.get('message', 'Unknown error')
            raise Exception(f"An exception occurred during listing projects: {msg}")

        if response.get('status') == 'success':
            projects_ids.extend(response.get('data', []))

    return projects_ids


def load_project(project_id, scope="user"):
    """
    Load a project by its ID.
    """
    response = JarvisPyClient.load_project(project_id=project_id, scope=scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during loading project: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during loading project: {response.get('message', 'Unknown error')}")








    


