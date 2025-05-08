from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Virtual Knowledge Graph Persistence Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


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


def cleanup_kg(virtual_kg=None):
    """
    Cleanup Virtual KG resources for the user.
    If `virtual_kg` is provided, it only cleans up resources for that KG.
    If `virtual_kg` is None, it cleans up all resources for the user associated with the PMTX token.
    """
    if virtual_kg is not None:
        delete_virtual_kg_resource_response = JarvisPyClient.cleanup_kg(virtual_kg)
    else:
        delete_virtual_kg_resource_response = JarvisPyClient.cleanup_kg()

    if delete_virtual_kg_resource_response.status_code != 200:
        msg = delete_virtual_kg_resource_response.json().get('message', 'Unknown error')
        raise Exception(f"HTTP error! status: {delete_virtual_kg_resource_response.get('status_code')}, detail: {msg}")
    else:
        print(delete_virtual_kg_resource_response.json().get('message', 'Unknown error'))


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


def load_kg_notebooks(virtual_kg):
    """
    Load all notebooks for a specific knowledge graph.
    """
    response = JarvisPyClient.load_kg_notebooks(virtual_kg)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during loading notebooks: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', [])
    else:
        raise Exception(f"An exception occurred during loading notebooks: {response.get('message', 'Unknown error')}")


def save_kg_notebook(virtual_kg, notebook_name, notebook_id = None):
    """
    Save a notebook for a specific knowledge graph.
    Returns the notebook_id of the saved notebook.
    """
    response = JarvisPyClient.save_kg_notebook(virtual_kg, notebook_id, notebook_name)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while saving notebook: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {}).get('notebook_id')
    else:
        raise Exception(f"An exception occurred while saving notebook: {response.get('message', 'Unknown error')}")


def cleanup_kg_notebooks(virtual_kg, notebook_ids=None):
    """
    Cleanup notebooks for a specific knowledge graph.
    If `notebook_ids` is provided, it only cleans up those specific notebooks.
    If `notebook_ids` is None, it cleans up all notebooks for the knowledge graph.
    """
    response = JarvisPyClient.cleanup_kg_notebooks(virtual_kg, notebook_ids)

    if response.status_code != 200:
        msg = response.json().get('message', 'Unknown error')
        raise Exception(f"HTTP error! status: {response.status_code}, detail: {msg}")
    else:
        print(response.json().get('message', 'Unknown error'))


def load_kg_cells(virtual_kg, notebook_id):
    """
    Load all cells for a specific notebook.
    """
    response = JarvisPyClient.load_kg_cells(virtual_kg, notebook_id)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during loading cells: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', [])
    else:
        raise Exception(f"An exception occurred during loading cells: {response.get('message', 'Unknown error')}")


def save_kg_cell(virtual_kg, notebook_id, cell_content, cell_position=1, cell_id=None):
    """
    Save a cell for a specific notebook.
    Returns the cell_id of the saved cell.
    """
    response = JarvisPyClient.save_kg_cell(virtual_kg, notebook_id, cell_id, cell_content, cell_position)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while saving cell: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {}).get('cell_id')
    else:
        raise Exception(f"An exception occurred while saving cell: {response.get('message', 'Unknown error')}")


def run_kg_cell(virtual_kg, notebook_id, cell_content, cell_position=1, cell_id=None):
    """
    Execute a cell in a notebook.
    Returns the cell_id of the executed cell.
    """
    response = JarvisPyClient.run_kg_cell(virtual_kg, notebook_id, cell_content, cell_position, cell_id)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while executing cell: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {})
    else:
        raise Exception(f"An exception occurred while executing cell: {response.get('message', 'Unknown error')}")


def cleanup_kg_cells(virtual_kg, notebook_id=None, cell_ids=None):
    """
    Cleanup cells for a specific knowledge graph or notebook.
    If `cell_ids` is provided, it only cleans up those specific cells.
    If `notebook_id` is provided but `cell_ids` is None, it cleans up all cells for that notebook.
    If both `notebook_id` and `cell_ids` are None, it cleans up all cells for the knowledge graph.
    """
    response = JarvisPyClient.cleanup_kg_cells(virtual_kg, notebook_id, cell_ids)

    if response.status_code != 200:
        msg = response.json().get('message', 'Unknown error')
        raise Exception(f"HTTP error! status: {response.status_code}, detail: {msg}")
    else:
        print(response.json().get('message', 'Unknown error'))
