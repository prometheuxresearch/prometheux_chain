"""
Chat History Management Module

Browse, load, rename, and delete persistent AI agent chat sessions.

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"Chat history {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def list_sessions(project_id=None, limit=50):
    """List recent chat sessions, newest first."""
    return _check(JarvisPyClient.list_sessions(project_id=project_id, limit=limit), "list sessions")


def get_session(session_id):
    """Load a full chat session including all its messages."""
    return _check(JarvisPyClient.get_session(session_id), "get session")


def rename_session(session_id, title):
    """Rename a chat session."""
    response = JarvisPyClient.rename_session(session_id, title)
    if response.get('status') != 'success':
        raise Exception(f"Chat history rename failed: {response.get('message', 'Unknown error')}")
    return response.get('message')


def delete_session(session_id):
    """Delete a chat session and all its messages."""
    response = JarvisPyClient.delete_session(session_id)
    if response.get('status') != 'success':
        raise Exception(f"Chat history delete failed: {response.get('message', 'Unknown error')}")
