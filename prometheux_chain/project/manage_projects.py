from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Project Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def cleanup_projects(workspace_id="workspace_id", project_id=None, project_scope="user"):
    """
    Cleanup project resources for the user.
    
    Args:
        workspace_id (str): The ID of the workspace (default: "workspace_id")
        project_id (str, optional): The ID of the specific project to cleanup. If None, cleans up all projects
        project_scope (str): The scope of the project (default: "user")
    
    Returns:
        None: Prints success message on completion
    
    Raises:
        Exception: If the cleanup fails or returns an error status
    """
    response = JarvisPyClient.cleanup_projects(workspace_id=workspace_id, project_id=project_id, project_scope=project_scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while cleaning up project: {msg}")
    
    if response.get('status') == 'success':
        print(response.get('message', 'Project resources cleaned up successfully'))
    else:
        raise Exception(f"An exception occurred while cleaning up project: {response.get('message', 'Unknown error')}") 
    

def save_project(workspace_id="workspace_id", project_id=None, project_name=None, project_scope="user"):
    """
    Save a project with the specified parameters.
    
    Args:
        workspace_id (str): The ID of the workspace (default: "workspace_id")
        project_id (str, optional): The ID of the project to save
        project_name (str, optional): The name of the project
        project_scope (str): The scope of the project (default: "user")
    
    Returns:
        str: The project ID of the saved project
    
    Raises:
        Exception: If the save operation fails or returns an error status
    """
    response = JarvisPyClient.save_project(workspace_id=workspace_id, project_id=project_id, project_name=project_name, project_scope=project_scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while saving project: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {}).get('project_id')
    else:
        raise Exception(f"An exception occurred while saving project: {response.get('message', 'Unknown error')}")


def list_projects(workspace_id="workspace_id", project_scopes=["user"]):
    """
    List all projects saved by the user.
    
    Args:
        workspace_id (str): The ID of the workspace (default: "workspace_id")
        project_scopes (list): List of project scopes to filter by (default: ["user"])
    
    Returns:
        list: List of project data dictionaries
    
    Raises:
        Exception: If the list operation fails or returns an error status
    """
    response = JarvisPyClient.list_projects(workspace_id=workspace_id, project_scopes=project_scopes)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while listing projects: {msg}")

    if response.get('status') == 'success':
        return response.get('data', [])
    else:
        raise Exception(f"An exception occurred while listing projects: {response.get('message', 'Unknown error')}")


def load_project(project_id, workspace_id="workspace_id", project_scope = "user"):
    """
    Load a project by its ID.
    
    Args:
        project_id (str): The ID of the project to load
        workspace_id (str): The ID of the workspace (default: "workspace_id")
        project_scope (str): The scope of the project (default: "user")
    
    Returns:
        dict: Project data dictionary or None if not found
    
    Raises:
        Exception: If the load operation fails or returns an error status
    """
    response = JarvisPyClient.load_project(workspace_id=workspace_id, project_id=project_id, project_scope=project_scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while loading project: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred while loading project: {response.get('message', 'Unknown error')}")


def copy_project(project_id, workspace_id="workspace_id", target_scope="user", new_project_name=None):
    """
    Copy a project to create a new project with the same content.
    
    Args:
        project_id (str): The ID of the project to copy
        workspace_id (str): The ID of the workspace (default: "workspace_id")
        target_scope (str): The scope for the copied project (default: "user")
        new_project_name (str, optional): The name for the new copied project
    
    Returns:
        dict: Response data containing information about the copied project
    
    Raises:
        Exception: If the copy operation fails or returns an error status
    """
    response = JarvisPyClient.copy_project(
        project_id=project_id,
        workspace_id=workspace_id,
        target_scope=target_scope,
        new_project_name=new_project_name
    )

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while copying project: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {})
    else:
        raise Exception(f"An exception occurred while copying project: {response.get('message', 'Unknown error')}")








    


