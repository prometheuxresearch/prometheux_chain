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


def cleanup_sources(source_ids=None):
    """Delete data sources by ID. If None, deletes all."""
    response = JarvisPyClient.cleanup_sources(source_ids)
    if response.get('status') != 'success':
        raise Exception(f"Source cleanup failed: {response.get('message', 'Unknown error')}")


def connect_sources(database_payload: Database = None, compute_row_count=False):
    """Connect a data source."""
    return _check(JarvisPyClient.connect_sources(
        database_payload=database_payload, compute_row_count=compute_row_count,
    ), "connect")


def list_sources():
    """List all connected data sources."""
    return _check(JarvisPyClient.list_sources(), "list")


def infer_schema(database: Database, add_bind=True, add_model=False):
    """Infer schema from a database connection."""
    return _check(JarvisPyClient.infer_schema(
        database, add_bind, add_model,
    ), "infer schema")
