"""
User Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from typing import Dict, Any

from ..client.jarvispy_client import JarvisPyClient


def save_user_config(config_data: Dict[str, Any], scope: str = "user") -> str:
    """Save user configuration."""
    response = JarvisPyClient.save_user_config(config_data, scope)
    return response.get("message", "Configuration saved successfully")


def load_user_config(scope: str = "user") -> Dict[str, Any]:
    """Load user configuration."""
    response = JarvisPyClient.load_user_config(scope)
    return response.get("data", {})
