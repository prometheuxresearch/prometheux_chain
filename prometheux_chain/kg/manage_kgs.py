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


def graph_rag(
    workspace_id="workspace_id",
    project_id=None,
    question=None,
    graph_selected_concepts=None,
    graph_available_concepts=None,
    rag_concepts=None,
    rag_records=None,
    project_scope="user",
    llm=None,
    top_k=5,
):
    """
    Unified GraphRAG wrapper with clean parameters for knowledge graph retrieval and generation.
    
    Args:
        workspace_id (str): The ID of the workspace (default: "workspace_id")
        project_id (str, optional): The ID of the project
        question (str, optional): The question to ask the GraphRAG system
        graph_selected_concepts (list, optional): List of concept names to be executed directly
        graph_available_concepts (list, optional): List of concept names available to the orchestrator
        rag_concepts (list, optional): List of dicts with concept and field_to_embed for retrieval
        rag_records (list, optional): List of records for RAG embedding retrieval
        project_scope (str): The scope of the project (default: "user")
        llm (dict, optional): LLM configuration dictionary
        top_k (int): Number of top results to retrieve (default: 5)
    
    Returns:
        dict: Response data from the GraphRAG query or None
    
    Raises:
        Exception: If the question is not provided or the GraphRAG query fails
    """
    if not question:
        raise Exception("question is required")

    graph_payload = None
    if graph_selected_concepts or graph_available_concepts:
        graph_payload = {}
        if graph_selected_concepts:
            graph_payload['selected_concepts'] = graph_selected_concepts
        if graph_available_concepts:
            graph_payload['available_concepts'] = graph_available_concepts

    rag_payload = None
    if rag_concepts or rag_records or top_k != 5:
        rag_payload = {}
        if rag_concepts:
            rag_payload['embedding_to_retrieve'] = rag_concepts
        if rag_records:
            rag_payload['embedding_retrieved'] = rag_records
        if top_k != 5:
            rag_payload['top_k'] = top_k

    response = JarvisPyClient.graph_rag(
        workspace_id=workspace_id,
        project_id=project_id,
        question=question,
        graph=graph_payload,
        rag=rag_payload,
        llm=llm,
        project_scope=project_scope,
    )

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during GraphRAG query: {msg}")
    
    return response.get('data', None)