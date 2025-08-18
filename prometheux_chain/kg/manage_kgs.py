from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
KG Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

def save_kg(workspace_id="workspace_id", project_id=None, concepts=None, scope="user"):
    """
    Save a virtual knowledge graph for a project.
    
    Args:
        workspace_id (str): The ID of the workspace
        project_id (str): The ID of the project
        kg_name (str): The name of the knowledge graph
        kg_concepts (list): List of concept names to include in the KG
        scope (str): The scope of the project (default: "user")
    
    Returns:
        dict: Response from the API containing the saved KG information
    """
    if not project_id:
        raise ValueError("project_id is required")
    
    if not concepts or not isinstance(concepts, list):
        raise ValueError("kg_concepts must be a non-empty list")
    
    return JarvisPyClient.save_kg(workspace_id=workspace_id, project_id=project_id, concepts=concepts, scope=scope)


def load_kg(workspace_id="workspace_id", project_id=None, scope="user"):
    """
    Load a virtual knowledge graph for a project.
    
    Args:
        workspace_id (str): The ID of the workspace
        project_id (str): The ID of the project
        scope (str): The scope of the project (default: "user")
    
    Returns:
        dict: Response from the API containing the loaded KG data including:
              - project_id: The project ID
              - name: The KG name
              - concepts: List of concepts in the KG
              - rules: List of rules in the KG
              - timestamp: When the KG was created/modified
              - author: Who created the KG
    """
    if not project_id:
        raise ValueError("project_id is required")
    
    return JarvisPyClient.load_kg(workspace_id, project_id, scope)