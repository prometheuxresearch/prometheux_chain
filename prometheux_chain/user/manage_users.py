"""
User Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from typing import Dict, Any

from ..client.jarvispy_client import JarvisPyClient


def save_user_config(config_data: Dict[str, Any]) -> str:
    """Save user configuration."""
    response = JarvisPyClient.save_user_config(config_data)
    return response.get("message", "Configuration saved successfully")


def load_user_config() -> Dict[str, Any]:
    """Load user configuration."""
    response = JarvisPyClient.load_user_config()
    return response.get("data", {})


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"User {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def get_role() -> Dict[str, Any]:
    """Get the authenticated user's role."""
    return _check(JarvisPyClient.get_role(), "get role")


def get_login_activity():
    """Get distinct IPs / sessions that have accessed this user's pod."""
    return _check(JarvisPyClient.get_login_activity(), "login activity")


def list_llm_models(provider: str, **credentials) -> Dict[str, Any]:
    """List available model names for a given LLM provider.

    Provider-specific credentials may be passed as keyword arguments.
    """
    return _check(JarvisPyClient.list_llm_models(provider, credentials or None), "list llm models")


def get_usage_status() -> Dict[str, Any]:
    """Get current LLM/embedding usage counts and limits."""
    return _check(JarvisPyClient.get_usage_status(), "usage status")
