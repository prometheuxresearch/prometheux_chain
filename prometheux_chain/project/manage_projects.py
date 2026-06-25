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


def copy_project(project_id, target_scope="user", new_project_name=None, compute=None):
    """Copy a project."""
    return _check(JarvisPyClient.copy_project(
        project_id=project_id, target_scope=target_scope,
        new_project_name=new_project_name, compute=compute,
    ), "copy")


def export_project(project_id=None, scope="user"):
    """Export a single project."""
    return _check(JarvisPyClient.export_project(
        project_id=project_id, scope=scope,
    ), "export")


def import_project(export_data, scope="user", force_new_id=False, compute=None):
    """Import a project from exported data."""
    if not export_data or not isinstance(export_data, dict):
        raise ValueError("export_data must be a non-empty dictionary")
    return _check(JarvisPyClient.import_project(
        export_data=export_data, scope=scope, force_new_id=force_new_id, compute=compute,
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


# ── Templates ─────────────────────────────────────────────────────────────

def list_templates():
    """List the available project templates from the marketplace."""
    return _check(JarvisPyClient.list_templates(), "list templates")


def import_template(template_id, new_project_name=None, project_scope="user", compute=None):
    """Create a new project from a marketplace template."""
    return _check(JarvisPyClient.import_template(
        template_id=template_id, new_project_name=new_project_name,
        project_scope=project_scope, compute=compute,
    ), "import template")


def create_project_from_context(context, scope="user", concept_names=None, file_paths=None):
    """Create a project from free-text context and optional file attachments.

    ``file_paths`` is a list of local file paths to upload alongside the context.
    """
    return _check(JarvisPyClient.create_project_from_context(
        context=context, scope=scope, concept_names=concept_names, file_paths=file_paths,
    ), "create from context")


# ── Snapshots (versioning) ─────────────────────────────────────────────────

def create_snapshot(project_id, scope="user", description=None):
    """Create a point-in-time snapshot of a project."""
    return _check(JarvisPyClient.create_snapshot(
        project_id=project_id, scope=scope, description=description,
    ), "create snapshot")


def list_snapshots(project_id, scope="user"):
    """List all snapshots for a project (metadata only)."""
    return _check(JarvisPyClient.list_snapshots(
        project_id=project_id, scope=scope,
    ), "list snapshots")


def restore_snapshot(snapshot_id, project_id, scope="user", create_safety_snapshot=True):
    """Restore a project from a previously saved snapshot."""
    return _check(JarvisPyClient.restore_snapshot(
        snapshot_id=snapshot_id, project_id=project_id, scope=scope,
        create_safety_snapshot=create_safety_snapshot,
    ), "restore snapshot")


def delete_snapshot(snapshot_id, project_id, scope="user"):
    """Delete a single snapshot."""
    response = JarvisPyClient.delete_snapshot(
        snapshot_id=snapshot_id, project_id=project_id, scope=scope,
    )
    if response.get('status') != 'success':
        raise Exception(f"Project delete snapshot failed: {response.get('message', 'Unknown error')}")
