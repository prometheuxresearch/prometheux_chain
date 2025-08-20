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
    persist_outputs=False
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
        persist_outputs=persist_outputs
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
    

def graph_rag(
    workspace_id="workspace_id",
    project_id=None,
    question=None,
    graph_concepts=None,
    rag_concepts=None,
    rag_records=None,
    project_scope="user",
    llm=None,
    top_k=5,
):
    """
    Unified GraphRAG wrapper with clean params.
    - graph_concepts: list[str] → added as graph.concepts if not empty
    - rag_concepts: list[{"concept": str, "field_to_embed": str}] → added as rag.embedding_to_retrieve if not empty
    - llm: optional LLM config dict; included if provided
    - top_k: optional int, defaults to 5 → added to rag config to control number of retrieved results
    """
    if not question:
        raise Exception("question is required")

    graph_payload = None
    if graph_concepts:
        graph_payload = { 'concepts': graph_concepts }

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