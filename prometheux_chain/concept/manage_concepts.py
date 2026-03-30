"""
Concept Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"Concept {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def save_concept(project_id, definition, python_scripts=None, scope="user",
                 description=None, concept_type="logic", concept_name=None,
                 binds=None, output_predicate="", existing_name=None,
                 position=None, group="group_id", compute=None):
    """Save a concept. Only ``definition`` is required; everything else has defaults."""
    return _check(JarvisPyClient.save_concept(
        project_id=project_id, definition=definition, python_scripts=python_scripts,
        scope=scope, description=description, concept_type=concept_type,
        concept_name=concept_name, binds=binds, output_predicate=output_predicate,
        existing_name=existing_name, position=position, group=group, compute=compute,
    ), "save")


def run_concept(project_id, concept_name, params=None, scope="user",
                force_rerun=True, persist_outputs=False, compute=None):
    """Run a concept. Only ``project_id`` and ``concept_name`` are required."""
    return _check(JarvisPyClient.run_concept(
        project_id=project_id, concept_name=concept_name,
        params=params or {}, scope=scope, force_rerun=force_rerun,
        persist_outputs=persist_outputs, compute=compute,
    ), "run")


def list_concepts(project_id, scope="user"):
    """List all concepts in a project."""
    return _check(JarvisPyClient.list_concepts(
        project_id=project_id, scope=scope,
    ), "list")


def cleanup_concepts(project_id, scope="user", concept_names=None):
    """Delete concepts from a project. If ``concept_names`` is None, deletes all."""
    return _check(JarvisPyClient.cleanup_concepts(
        project_id=project_id, scope=scope, concept_names=concept_names,
    ), "cleanup")


def fetch_results(project_id, output_predicate, page=1, page_size=10,
                  scope="user", order_by=None):
    """Fetch paginated results for a populated predicate."""
    return _check(JarvisPyClient.fetch_results(
        project_id=project_id, output_predicate=output_predicate,
        page=page, page_size=page_size, scope=scope, order_by=order_by,
    ), "fetch")
