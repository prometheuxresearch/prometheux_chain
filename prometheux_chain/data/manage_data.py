from prometheux_chain.client.jarvispy_client import JarvisPyClient
from prometheux_chain.data.database import Database

"""
Data Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def cleanup_sources(source_ids=None):
    """
    Cleanup sources for a workspace.
    
    Args:
        source_ids (list, optional): List of source IDs to cleanup. If None, cleans up all sources
    
    Returns:
        None: Prints success message on completion
    
    Raises:
        Exception: If the cleanup fails or returns an error status
    """
    response = JarvisPyClient.cleanup_sources(source_ids)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during cleaning up sources: {msg}")
    
    if response.get('status') == 'success':
        print(response.get('message', 'Project sources cleaned up successfully'))
    else:
        raise Exception(f"An exception occurred during cleaning up sources: {response.get('message', 'Unknown error')}")


def connect_sources(database_payload:Database=None, compute_row_count=False):
    """
    Connect a source to a workspace.
    
    Args:
        database_payload (Database, optional): Database configuration object
        compute_row_count (bool): Whether to compute row count during connection (default: False)
    
    Returns:
        dict: Response data from the connection operation or None
    
    Raises:
        Exception: If the connection fails or returns an error status
    """
    response = JarvisPyClient.connect_sources(database_payload=database_payload, compute_row_count=compute_row_count)
    
    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during connecting sources: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during connecting sources: {response.get('message', 'Unknown error')}")
    

def list_sources():
    """
    List sources for a workspace.
    
    Args:
    
    Returns:
        list: List of source data dictionaries
    
    Raises:
        Exception: If the list operation fails or returns an error status
    """
    response = JarvisPyClient.list_sources()

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during listing sources: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', [])
    else:
        raise Exception(f"An exception occurred during listing sources: {response.get('message', 'Unknown error')}")
    

def infer_schema(database:Database, add_bind=True, add_model=False):
    """
    Infer schema from a database connection.
    
    Args:
        database (Database): Database configuration object
        add_bind (bool): Whether to add bind information (default: True)
        add_model (bool): Whether to add model information (default: False)
    
    Returns:
        dict: Response data containing inferred schema information or None
    
    Raises:
        Exception: If the schema inference fails or returns an error status
    """
    response = JarvisPyClient.infer_schema(database, add_bind, add_model)
    
    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during inferring schema: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', None)
    else:
        raise Exception(f"An exception occurred during inferring schema: {response.get('message', 'Unknown error')}")