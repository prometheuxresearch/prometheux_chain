from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Virtual Knowledge Graph Persistence Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""



def cleanup_kg(virtual_kg=None):
    """
    Cleanup Virtual KG resources for the user.
    If `virtual_kg` is provided, it only cleans up resources for that KG.
    If `virtual_kg` is None, it cleans up all resources for the user associated with the PMTX token.
    """
    if virtual_kg is not None:
        delete_virtual_kg_resource_response = JarvisPyClient.cleanup(virtual_kg)
    else:
        delete_virtual_kg_resource_response = JarvisPyClient.cleanup()

    if delete_virtual_kg_resource_response.status_code != 200:
        msg = delete_virtual_kg_resource_response.json().get('message', 'Unknown error')
        raise Exception(f"HTTP error! status: {delete_virtual_kg_resource_response.get('status_code')}, detail: {msg}")
    else:
        print(delete_virtual_kg_resource_response.json().get('message', 'Unknown error'))


def save_kg(virtual_kg):
    """
    Save a virtual knowledge graph.
    """
    response = JarvisPyClient.save(virtual_kg)

    # Handle response codes
    if response.status_code != 200:
        msg = response.json().get('message', 'Unknown error')
        raise Exception(f"An exception occurred while saving knowledge graph: {msg}")
    else:
        print(response.json().get('message', 'Unknown error'))

def list_kgs():
    """
    List all knowledge graphs saved by the user.
    """
    response = JarvisPyClient.list_kgs()

    # Handle response codes
    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during listing knowledge graphs: {msg}")

    if response.get('status') == 'success':
        return response.get('data', [])
    else:
        raise Exception(f"An exception occurred during listing knowledge graphs: {response.get('message', 'Unknown error')}")


def load_kg(kg_id):
    """
    Load a knowledge graph by its ID.
    """
    response = JarvisPyClient.load(kg_id)

    # Handle response codes
    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during loading knowledge graph: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during loading knowledge graph: {response.get('message', 'Unknown error')}")


def load_kg_chat(kg_id):
    """
    Load chat interactions for a specific knowledge graph by its ID.
    """
    response = JarvisPyClient.load_kg_chat(kg_id)

    # Handle response
    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during loading chat interactions: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', [])
    else:
        raise Exception(f"An exception occurred during loading chat interactions: {response.get('message', 'Unknown error')}")


def cleanup_kg_chat(kg_id, chat_ids=None):
    """
    Cleanup chat interactions for a specific knowledge graph.
    If `chat_ids` is provided, it only cleans up those specific chat interactions.
    If `chat_ids` is None, it cleans up all chat interactions for the knowledge graph.
    """
    response = JarvisPyClient.cleanup_kg_chat(kg_id, chat_ids)

    if response.status_code != 200:
        msg = response.json().get('message', 'Unknown error')
        raise Exception(f"HTTP error! status: {response.status_code}, detail: {msg}")
    else:
        print(response.json().get('message', 'Unknown error'))


def save_kg_chat(kg_id, prompt, response_text):
    """
    Save a chat interaction for a specific knowledge graph.
    Returns the chat_id of the saved interaction.
    """
    response = JarvisPyClient.save_kg_chat(kg_id, prompt, response_text)

    # Handle response
    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while saving chat interaction: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {}).get('chat_id')
    else:
        raise Exception(f"An exception occurred while saving chat interaction: {response.get('message', 'Unknown error')}")


