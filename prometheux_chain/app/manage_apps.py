"""
App Management Module

CRUD for user-defined apps within an ontology.

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"App {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def list_all_apps(scope="user"):
    """List metadata for all apps across all ontologies."""
    return _check(JarvisPyClient.list_all_apps(scope=scope), "list all")


def list_apps(ontology_id, scope="user"):
    """List metadata for all apps in an ontology."""
    return _check(JarvisPyClient.list_apps(ontology_id=ontology_id, scope=scope), "list")


def get_app(ontology_id, app_id, scope="user"):
    """Load a single app with its full definition."""
    return _check(JarvisPyClient.get_app(
        ontology_id=ontology_id, app_id=app_id, scope=scope,
    ), "get")


def save_app(ontology_id, app, scope="user"):
    """Create or update an app. Returns the assigned app id."""
    return _check(JarvisPyClient.save_app(
        ontology_id=ontology_id, app=app, scope=scope,
    ), "save")


def delete_app(ontology_id, app_id, scope="user"):
    """Permanently delete an app."""
    response = JarvisPyClient.delete_app(
        ontology_id=ontology_id, app_id=app_id, scope=scope,
    )
    if response.get('status') != 'success':
        raise Exception(f"App delete failed: {response.get('message', 'Unknown error')}")
