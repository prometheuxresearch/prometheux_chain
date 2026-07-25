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


def save_ontology(ontology_id=None, ontology_name=None, ontology_scope="user", description=None):
    """Save or create a project."""
    data = _check(JarvisPyClient.save_ontology(
        ontology_id=ontology_id, ontology_name=ontology_name,
        ontology_scope=ontology_scope, description=description,
    ), "save")
    return data.get('project_id') if isinstance(data, dict) else data


def list_ontologies(ontology_scopes=None):
    """List all projects for the given scopes."""
    return _check(JarvisPyClient.list_ontologies(
        ontology_scopes=ontology_scopes or ["user"],
    ), "list")


def load_ontology(ontology_id, ontology_scope="user"):
    """Load a project by ID."""
    return _check(JarvisPyClient.load_ontology(
        ontology_id=ontology_id, ontology_scope=ontology_scope,
    ), "load")


def cleanup_ontologies(ontology_id=None, ontology_scope="user"):
    """Delete a project and its resources."""
    response = JarvisPyClient.cleanup_ontologies(ontology_id=ontology_id, ontology_scope=ontology_scope)
    if response.get('status') != 'success':
        raise Exception(f"Project cleanup failed: {response.get('message', 'Unknown error')}")


def copy_ontology(ontology_id, target_scope="user", new_ontology_name=None, compute=None):
    """Copy a project."""
    return _check(JarvisPyClient.copy_ontology(
        ontology_id=ontology_id, target_scope=target_scope,
        new_ontology_name=new_ontology_name, compute=compute,
    ), "copy")


def export_ontology(ontology_id=None, scope="user"):
    """Export a single project."""
    return _check(JarvisPyClient.export_ontology(
        ontology_id=ontology_id, scope=scope,
    ), "export")


def import_ontology(export_data, scope="user", force_new_id=False, compute=None):
    """Import a project from exported data."""
    if not export_data or not isinstance(export_data, dict):
        raise ValueError("export_data must be a non-empty dictionary")
    return _check(JarvisPyClient.import_ontology(
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


def import_template(template_id, new_ontology_name=None, ontology_scope="user", compute=None):
    """Create a new project from a marketplace template."""
    return _check(JarvisPyClient.import_template(
        template_id=template_id, new_ontology_name=new_ontology_name,
        ontology_scope=ontology_scope, compute=compute,
    ), "import template")


def create_ontology_from_context(context, scope="user", concept_names=None, file_paths=None):
    """Create a project from free-text context and optional file attachments.

    ``file_paths`` is a list of local file paths to upload alongside the context.
    """
    return _check(JarvisPyClient.create_ontology_from_context(
        context=context, scope=scope, concept_names=concept_names, file_paths=file_paths,
    ), "create from context")


# ── Snapshots (versioning) ─────────────────────────────────────────────────

def create_snapshot(ontology_id, scope="user", description=None):
    """Create a point-in-time snapshot of a project."""
    return _check(JarvisPyClient.create_snapshot(
        ontology_id=ontology_id, scope=scope, description=description,
    ), "create snapshot")


def list_snapshots(ontology_id, scope="user"):
    """List all snapshots for a project (metadata only)."""
    return _check(JarvisPyClient.list_snapshots(
        ontology_id=ontology_id, scope=scope,
    ), "list snapshots")


def restore_snapshot(snapshot_id, ontology_id, scope="user", create_safety_snapshot=True):
    """Restore a project from a previously saved snapshot."""
    return _check(JarvisPyClient.restore_snapshot(
        snapshot_id=snapshot_id, ontology_id=ontology_id, scope=scope,
        create_safety_snapshot=create_safety_snapshot,
    ), "restore snapshot")


def delete_snapshot(snapshot_id, ontology_id, scope="user"):
    """Delete a single snapshot."""
    response = JarvisPyClient.delete_snapshot(
        snapshot_id=snapshot_id, ontology_id=ontology_id, scope=scope,
    )
    if response.get('status') != 'success':
        raise Exception(f"Project delete snapshot failed: {response.get('message', 'Unknown error')}")
