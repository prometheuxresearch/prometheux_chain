from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Virtual Knowledge Graph Persistence Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def cleanup_kgs(project_id, project_scope="user", kg_ids=None):
    """
    Cleanup Virtual KG resources for the user.
    If `kg_ids` is provided, it only cleans up resources for those specific KGs.
    If `kg_ids` is None, it cleans up all resources for the project.
    """
    response = JarvisPyClient.cleanup_kgs(project_id, project_scope, kg_ids)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during cleaning up virtual knowledge graphs: {msg}")
    
    if response.get('status') == 'success':
        print(response.get('message', 'Virtual knowledge graphs cleaned up successfully'))
    else:
        raise Exception(f"An exception occurred during cleaning up virtual knowledge graphs: {response.get('message', 'Unknown error')}")
    



















def save_kg(virtual_kg):
    """
    Save a virtual knowledge graph.
    """
    response = JarvisPyClient.save_kg(virtual_kg)

    if response.status_code != 200:
        msg = response.json().get('message', 'Unknown error')
        raise Exception(f"An exception occurred while saving knowledge graph: {msg}")
    else:
        print(response.json().get('message', 'Unknown error'))


def list_kgs(scopes=["user"]):
    """
    List all knowledge graphs saved by the user.
    """
    response = JarvisPyClient.list_kgs(scopes)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during listing knowledge graphs: {msg}")

    if response.get('status') == 'success':
        return response.get('data', [])
    else:
        raise Exception(f"An exception occurred during listing knowledge graphs: {response.get('message', 'Unknown error')}")


def load_kg(virtual_kg):
    """
    Load a knowledge graph by its ID.
    """
    response = JarvisPyClient.load_kg(virtual_kg)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during loading knowledge graph: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during loading knowledge graph: {response.get('message', 'Unknown error')}")




def save_kg_chat(virtual_kg, prompt, response):
    """
    Save a chat interaction for a specific knowledge graph.
    Returns the chat_id of the saved interaction.
    """
    response = JarvisPyClient.save_kg_chat(virtual_kg, prompt, response)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while saving chat interaction: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {}).get('chat_id')
    else:
        raise Exception(f"An exception occurred while saving chat interaction: {response.get('message', 'Unknown error')}")


def load_kg_chat(virtual_kg):
    """
    Load chat interactions for a specific knowledge graph by its ID.
    """
    response = JarvisPyClient.load_kg_chat(virtual_kg)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during loading chat interactions: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', [])
    else:
        raise Exception(f"An exception occurred during loading chat interactions: {response.get('message', 'Unknown error')}")


def cleanup_kg_chat(virtual_kg, chat_ids=None):
    """
    Cleanup chat interactions for a specific knowledge graph.
    If `chat_ids` is provided, it only cleans up those specific chat interactions.
    If `chat_ids` is None, it cleans up all chat interactions for the knowledge graph.
    """
    response = JarvisPyClient.cleanup_kg_chat(virtual_kg, chat_ids)

    if response.status_code != 200:
        msg = response.json().get('message', 'Unknown error')
        raise Exception(f"HTTP error! status: {response.status_code}, detail: {msg}")
    else:
        print(response.json().get('message', 'Unknown error'))


def save_kg_query(virtual_kg, query_logic, query_id=None):
    """
    Save a query for a specific knowledge graph.
    Returns the query_id of the saved query.
    """
    response = JarvisPyClient.save_kg_query(virtual_kg, query_id, query_logic)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while saving query: {msg}")

    if response.get('status') == 'success':
        return response.get('data', {}).get('query_id')
    else:
        raise Exception(f"An exception occurred while saving query: {response.get('message', 'Unknown error')}")


def load_kg_queries(virtual_kg):
    """
    Load all queries for a specific knowledge graph.
    """
    response = JarvisPyClient.load_kg_queries(virtual_kg)    

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during loading queries: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)   
    else:
        raise Exception(f"An exception occurred during loading queries: {response.get('message', 'Unknown error')}")


def cleanup_kg_queries(virtual_kg, query_ids=None):
    """
    Cleanup queries for a specific knowledge graph.
    """
    response = JarvisPyClient.cleanup_kg_queries(virtual_kg, query_ids)

    if response.status_code != 200:
        msg = response.json().get('message', 'Unknown error')
        raise Exception(f"HTTP error! status: {response.status_code}, detail: {msg}")
    else:
        print(response.json().get('message', 'Unknown error'))


