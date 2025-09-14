from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Concept Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def cleanup_concepts(workspace_id="workspace_id", project_id=None, project_scope="user"):
    """
    Cleanup concepts for a specific project.
    
    Args:
        workspace_id (str): The ID of the workspace (default: "workspace_id")
        project_id (str, optional): The ID of the project to cleanup concepts for
        project_scope (str): The scope of the project (default: "user")
    
    Returns:
        dict: Response data from the cleanup operation or None
    
    Raises:
        Exception: If the cleanup fails or returns an error status
    """
    response = JarvisPyClient.cleanup_concepts(workspace_id=workspace_id, project_id=project_id, project_scope=project_scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during cleaning up concepts: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during cleaning up concepts: {response.get('message', 'Unknown error')}")


def save_concept(workspace_id="workspace_id", project_id=None, concept_logic=None, python_scripts=None, scope="user"):
    """
    Save concept logic for a specific project.
    
    Args:
        workspace_id (str): The ID of the workspace (default: "workspace_id")
        project_id (str, optional): The ID of the project to save the concept for
        concept_logic (str, optional): The concept logic to save
        python_scripts (str, optional): Python scripts associated with the concept
        scope (str): The scope of the project (default: "user")
    
    Returns:
        dict: Response data from the save operation or None
    
    Raises:
        Exception: If the save operation fails or returns an error status
    """
    response = JarvisPyClient.save_concept(
        workspace_id=workspace_id,
        project_id=project_id,
        concept_logic=concept_logic,
        python_scripts=python_scripts,
        scope=scope
    )

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during saving concepts: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during saving concepts: {response.get('message', 'Unknown error')}")


def run_concept(
    workspace_id="workspace_id",
    project_id=None,
    concept_name=None,
    params=None,
    project_scope="user",
    step_by_step=False,
    materialize_intermediate_concepts=False,
    force_rerun=True,
    persist_outputs=False
):
    """
    Run a concept for a specific project.
    
    Args:
        workspace_id (str): The ID of the workspace (default: "workspace_id")
        project_id (str, optional): The ID of the project to run the concept in
        concept_name (str, optional): The name of the concept to run
        params (dict, optional): Parameters to pass to the concept
        project_scope (str): The scope of the project (default: "user")
        step_by_step (bool): Whether to run the concept step by step (default: False)
        materialize_intermediate_concepts (bool): Whether to materialize intermediate concepts (default: False)
        force_rerun (bool): Whether to force rerun the concept (default: True)
        persist_outputs (bool): Whether to persist outputs (default: False)
    
    Returns:
        dict: Response data from the concept execution or None
    
    Raises:
        Exception: If the concept execution fails or returns an error status
    """
    response = JarvisPyClient.run_concept(
        workspace_id=workspace_id,
        project_id=project_id,
        concept_name=concept_name,
        params=params or {},
        project_scope=project_scope,
        step_by_step=step_by_step,
        materialize_intermediate_concepts=materialize_intermediate_concepts,
        force_rerun=force_rerun,
        persist_outputs=persist_outputs,
    )

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during running concept: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during running concept: {response.get('message', 'Unknown error')}")


def list_concepts(workspace_id="workspace_id", project_id=None, project_scope="user"):
    """
    List all concepts for a specific project.
    
    Args:
        workspace_id (str): The ID of the workspace (default: "workspace_id")
        project_id (str, optional): The ID of the project to list concepts for
        project_scope (str): The scope of the project (default: "user")
    
    Returns:
        dict: Response data containing the list of concepts or None
    
    Raises:
        Exception: If the list operation fails or returns an error status
    """
    response = JarvisPyClient.list_concepts(workspace_id=workspace_id, project_id=project_id, project_scope=project_scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during listing concepts: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during listing concepts: {response.get('message', 'Unknown error')}") 