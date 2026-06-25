"""
Alert Management Module

Browse alert history and manually reprocess alerts (re-execute their concepts).

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"Alert {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def get_alert_history(limit=100, offset=0, scope="user"):
    """Retrieve historical alerts (paginated)."""
    return _check(JarvisPyClient.get_alert_history(
        limit=limit, offset=offset, scope=scope,
    ), "history")


def reprocess_alert(alert_id, scope="user", compute=None):
    """Reprocess an alert, re-executing its associated concept."""
    return _check(JarvisPyClient.reprocess_alert(
        alert_id=alert_id, scope=scope, compute=compute,
    ), "reprocess")
