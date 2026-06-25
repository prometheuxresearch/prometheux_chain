"""
Agent Management Module

Stream chat with the Vadalog AI agent and reset conversation sessions.

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def agent_chat(project_id, message, session_id=None, model=None, attachment_paths=None):
    """Send a message to the Vadalog AI agent and stream the response.

    Returns a generator yielding NDJSON events (dicts with a ``type`` key, e.g.
    ``metadata``, ``content``, ``tool_start``, ``proposal``, ``done``, ``error``).

    ``attachment_paths`` are ``disk/<name>`` paths previously returned by
    ``upload_file``.
    """
    return JarvisPyClient.agent_chat(
        project_id=project_id, message=message, session_id=session_id,
        model=model, attachment_paths=attachment_paths,
    )


def agent_reset(project_id, session_id=None):
    """Reset (clear) an agent conversation session."""
    response = JarvisPyClient.agent_reset(project_id=project_id, session_id=session_id)
    if response.get('status') != 'success':
        raise Exception(f"Agent reset failed: {response.get('message', 'Unknown error')}")
    return response.get('message')
