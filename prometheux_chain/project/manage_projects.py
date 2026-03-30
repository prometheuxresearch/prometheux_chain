"""
Project Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"Project {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def save_project(project_id=None, project_name=None, project_scope="user", description=None):
    """Save or create a project."""
    data = _check(JarvisPyClient.save_project(
        project_id=project_id, project_name=project_name,
        project_scope=project_scope, description=description,
    ), "save")
    return data.get('project_id') if isinstance(data, dict) else data


def list_projects(project_scopes=None):
    """List all projects for the given scopes."""
    return _check(JarvisPyClient.list_projects(
        project_scopes=project_scopes or ["user"],
    ), "list")


def load_project(project_id, project_scope="user"):
    """Load a project by ID."""
    return _check(JarvisPyClient.load_project(
        project_id=project_id, project_scope=project_scope,
    ), "load")


def cleanup_projects(project_id=None, project_scope="user"):
    """Delete a project and its resources."""
    response = JarvisPyClient.cleanup_projects(project_id=project_id, project_scope=project_scope)
    if response.get('status') != 'success':
        raise Exception(f"Project cleanup failed: {response.get('message', 'Unknown error')}")


def copy_project(project_id, target_scope="user", new_project_name=None):
    """Copy a project."""
    return _check(JarvisPyClient.copy_project(
        project_id=project_id, target_scope=target_scope,
        new_project_name=new_project_name,
    ), "copy")


def export_project(project_id=None, scope="user"):
    """Export a single project."""
    return _check(JarvisPyClient.export_project(
        project_id=project_id, scope=scope,
    ), "export")


def import_project(export_data, scope="user"):
    """Import a project from exported data."""
    if not export_data or not isinstance(export_data, dict):
        raise ValueError("export_data must be a non-empty dictionary")
    return _check(JarvisPyClient.import_project(
        export_data=export_data, scope=scope,
    ), "import")


def export_workspace(scope="user"):
    """Export the entire workspace."""
    return _check(JarvisPyClient.export_workspace(scope=scope), "workspace export")


def import_workspace(export_data, scope="user"):
    """Import an entire workspace from exported data."""
    if not export_data or not isinstance(export_data, dict):
        raise ValueError("export_data must be a non-empty dictionary")
    return _check(JarvisPyClient.import_workspace(
        export_data=export_data, scope=scope,
    ), "workspace import")
