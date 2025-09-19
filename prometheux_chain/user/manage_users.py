from typing import Dict, Any
from ..client.jarvispy_client import JarvisPyClient

"""
User Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def save_user_config(config_data: Dict[str, Any], scope: str = "user") -> str:
    """
    Save user configuration.
    
    Args:
        config_data (Dict[str, Any]): The configuration data to save
        scope (str): The scope of the configuration
        
    Returns:
        str: Success message
    """
    response = JarvisPyClient.save_user_config(config_data, scope)
    return response.get("message", "Configuration saved successfully")


def load_user_config(scope: str = "user") -> Dict[str, Any]:
    """
    Load user configuration.
    
    Args:
        scope (str): The scope of the configuration to load
        
    Returns:
        Dict[str, Any]: The loaded configuration data
    """
    response = JarvisPyClient.load_user_config(scope)
    return response.get("data", {})

