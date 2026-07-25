"""
Dashboard Management Module

CRUD for user-defined dashboards within a project.

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"Dashboard {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def list_all_dashboards(scope="user"):
    """List metadata for all dashboards across all projects."""
    return _check(JarvisPyClient.list_all_dashboards(scope=scope), "list all")


def list_dashboards(ontology_id, scope="user"):
    """List metadata for all dashboards in a project."""
    return _check(JarvisPyClient.list_dashboards(ontology_id=ontology_id, scope=scope), "list")


def get_dashboard(ontology_id, dashboard_id, scope="user"):
    """Load a single dashboard with its full definition."""
    return _check(JarvisPyClient.get_dashboard(
        ontology_id=ontology_id, dashboard_id=dashboard_id, scope=scope,
    ), "get")


def save_dashboard(ontology_id, dashboard, scope="user"):
    """Create or update a dashboard. Returns the assigned dashboard id."""
    return _check(JarvisPyClient.save_dashboard(
        ontology_id=ontology_id, dashboard=dashboard, scope=scope,
    ), "save")


def delete_dashboard(ontology_id, dashboard_id, scope="user"):
    """Permanently delete a dashboard."""
    response = JarvisPyClient.delete_dashboard(
        ontology_id=ontology_id, dashboard_id=dashboard_id, scope=scope,
    )
    if response.get('status') != 'success':
        raise Exception(f"Dashboard delete failed: {response.get('message', 'Unknown error')}")
