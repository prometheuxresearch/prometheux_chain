from ..config import config
from ..client.jarvispy_client import JarvisPyClient
import requests
import os

def kg_overview(virtual_kg):
    """
    Get an overview of a knowledge graph showing concepts with their column count and data information.
    
    Args:
        virtual_kg (dict): The virtual knowledge graph object. Must contain an 'id' field.
        
    Returns:
        dict: Overview data containing concepts with their column and data information.
        
    Raises:
        Exception: If PMTX_TOKEN is not set or if the API request fails.
    """
    if not virtual_kg:
        raise ValueError("Missing 'virtual_kg' parameter")
    
    return JarvisPyClient.kg_overview(virtual_kg)