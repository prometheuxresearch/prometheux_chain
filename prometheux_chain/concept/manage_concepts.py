from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Concept Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def cleanup_concepts(workspace_id="workspace_id", project_id=None, project_scope="user"):
    """
    Cleanup concepts for a specific project.
    """
    response = JarvisPyClient.cleanup_concepts(workspace_id=workspace_id, project_id=project_id, project_scope=project_scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during cleaning up concepts: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during cleaning up concepts: {response.get('message', 'Unknown error')}")


def save_concept(workspace_id="workspace_id", project_id=None, concept_logic=None, scope="user"):
    """
    Save concept logic for a specific project.
    """
    response = JarvisPyClient.save_concept(
        workspace_id=workspace_id,
        project_id=project_id,
        concept_logic=concept_logic,
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
    persist_outputs=False,
    python_scripts=None
):
    """
    Run a concept for a specific project.
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
        python_scripts=python_scripts
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
    """
    response = JarvisPyClient.list_concepts(workspace_id=workspace_id, project_id=project_id, project_scope=project_scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during listing concepts: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during listing concepts: {response.get('message', 'Unknown error')}") 