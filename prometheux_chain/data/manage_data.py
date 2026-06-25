"""
Data Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient
from ..data.database import Database


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"Data {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def cleanup_sources(source_ids=None, scope="user"):
    """Delete data sources by ID. If None, deletes all."""
    response = JarvisPyClient.cleanup_sources(source_ids=source_ids, scope=scope)
    if response.get('status') != 'success':
        raise Exception(f"Source cleanup failed: {response.get('message', 'Unknown error')}")


def connect_sources(database_payload: Database = None, compute_row_count=False, scope="user"):
    """Connect a data source."""
    return _check(JarvisPyClient.connect_sources(
        database_payload=database_payload, compute_row_count=compute_row_count, scope=scope,
    ), "connect")


def list_sources(scope="user"):
    """List all connected data sources."""
    return _check(JarvisPyClient.list_sources(scope=scope), "list")


def infer_schema(database: Database, add_bind=True, add_model=False):
    """Infer schema from a database connection."""
    return _check(JarvisPyClient.infer_schema(
        database, add_bind, add_model,
    ), "infer schema")


def list_sheets(database: Database):
    """List the sheets available in a spreadsheet-style data source."""
    return _check(JarvisPyClient.list_sheets(database), "list sheets")


def list_demo_sources():
    """List the Prometheux demo (px) data sources offered during onboarding."""
    return _check(JarvisPyClient.list_demo_sources(), "list demo sources")


def refresh_sources(scope="user", group_filter=None):
    """Re-connect every stored data-source group and reconcile the list."""
    return _check(JarvisPyClient.refresh_sources(scope=scope, group_filter=group_filter), "refresh")


def preview_datasource(bind_annotation, scope="user", limit=10, page=1, page_size=0,
                       order_by=None, search_term=None, column_filters=None, compute=None):
    """Preview rows from a data source described by a bind annotation."""
    return _check(JarvisPyClient.preview_datasource(
        bind_annotation=bind_annotation, scope=scope, limit=limit, page=page,
        page_size=page_size, order_by=order_by, search_term=search_term,
        column_filters=column_filters, compute=compute,
    ), "preview")


def all_pairs_join(database_payloads, to_evaluate=False, parallel=True):
    """Compute joinability across all pairs of the given data sources."""
    return _check(JarvisPyClient.all_pairs_join(
        database_payloads=database_payloads, to_evaluate=to_evaluate, parallel=parallel,
    ), "all pairs join")


# ── File management (disk/) ────────────────────────────────────────────────

def upload_file(file_path, path=""):
    """Upload a local file to the workspace disk/ storage."""
    return _check(JarvisPyClient.upload_file(file_path=file_path, path=path), "upload file")


def list_files(path=""):
    """List files and directories under the workspace disk/ storage."""
    return _check(JarvisPyClient.list_files(path=path), "list files")


def make_directory(path):
    """Create a new directory under the workspace disk/ storage."""
    return _check(JarvisPyClient.make_directory(path=path), "make directory")


def delete_files(paths, recursive=False):
    """Delete files or directories under the workspace disk/ storage."""
    return _check(JarvisPyClient.delete_files(paths=paths, recursive=recursive), "delete files")


def move_file(source, destination):
    """Move or rename a file under the workspace disk/ storage."""
    return _check(JarvisPyClient.move_file(source=source, destination=destination), "move file")


def download_file(path, dest_path=None):
    """Download a file from the workspace disk/ storage to a local path.

    Returns the local path the file was written to.
    """
    return JarvisPyClient.download_file(path=path, dest_path=dest_path)
