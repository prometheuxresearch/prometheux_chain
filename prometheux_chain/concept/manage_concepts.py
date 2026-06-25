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
                 position=None, group="group_id", compute=None, force_overwrite=False):
    """Save a concept. Only ``definition`` is required; everything else has defaults."""
    return _check(JarvisPyClient.save_concept(
        project_id=project_id, definition=definition, python_scripts=python_scripts,
        scope=scope, description=description, concept_type=concept_type,
        concept_name=concept_name, binds=binds, output_predicate=output_predicate,
        existing_name=existing_name, position=position, group=group, compute=compute,
        force_overwrite=force_overwrite,
    ), "save")


def rename_concept(project_id, old_name, new_name, scope="user"):
    """Rename a concept and propagate the change to all dependents."""
    return _check(JarvisPyClient.rename_concept(
        project_id=project_id, old_name=old_name, new_name=new_name, scope=scope,
    ), "rename")


def run_concept(project_id, concept_name, params=None, scope="user",
                force_rerun=True, persist_outputs=False, compute=None):
    """Run a concept. Only ``project_id`` and ``concept_name`` are required."""
    return _check(JarvisPyClient.run_concept(
        project_id=project_id, concept_name=concept_name,
        params=params or {}, scope=scope, force_rerun=force_rerun,
        persist_outputs=persist_outputs, compute=compute,
    ), "run")


def run_concept_stream(project_id, concept_name, params=None, scope="user",
                       force_rerun=True, persist_outputs=False, compute=None):
    """Run a concept and yield streaming status events over a WebSocket.

    Yields the raw server messages (dicts with an ``event`` key, e.g.
    ``concept_status``, ``complete``, ``error``). Iteration ends after the
    terminal ``complete`` or ``error`` event.
    """
    return JarvisPyClient.run_concept_stream(
        project_id=project_id, concept_name=concept_name,
        params=params or {}, scope=scope, force_rerun=force_rerun,
        persist_outputs=persist_outputs, compute=compute,
    )


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


def reorder_concepts(project_id, concept_names, scope="user", group=None):
    """Reorder concepts within a project (optionally within a group)."""
    return _check(JarvisPyClient.reorder_concepts(
        project_id=project_id, concept_names=concept_names, scope=scope, group=group,
    ), "reorder")


def get_execution_statuses(scopes="user"):
    """Return the latest non-idle run per project across the given scopes."""
    return _check(JarvisPyClient.get_execution_statuses(scopes=scopes), "execution statuses")


def get_execution_status(project_id, scope="user"):
    """Return the latest concept-run snapshot for a project."""
    return _check(JarvisPyClient.get_execution_status(
        project_id=project_id, scope=scope,
    ), "execution status")


def generate_concept_description(project_id, concept_name, scope="user"):
    """Generate (and cache) a natural-language description for a concept."""
    return _check(JarvisPyClient.generate_concept_description(
        project_id=project_id, concept_name=concept_name, scope=scope,
    ), "generate description")


def get_concept_description(project_id, concept_name, scope="user"):
    """Read back a concept's description, regenerating it if stale."""
    return _check(JarvisPyClient.get_concept_description(
        project_id=project_id, concept_name=concept_name, scope=scope,
    ), "get description")


def fetch_results(project_id, output_predicate, page=1, page_size=10,
                  scope="user", order_by=None, params=None, compute=None):
    """Fetch paginated results for a populated predicate."""
    return _check(JarvisPyClient.fetch_results(
        project_id=project_id, output_predicate=output_predicate,
        page=page, page_size=page_size, scope=scope, order_by=order_by,
        params=params, compute=compute,
    ), "fetch")


def search_results(project_id, output_predicate, search_term=None, column_filters=None,
                   scope="user", page=1, page_size=0, order_by=None, compute=None):
    """Search a populated predicate by free text and/or column filters."""
    return _check(JarvisPyClient.search_results(
        project_id=project_id, output_predicate=output_predicate,
        search_term=search_term, column_filters=column_filters, scope=scope,
        page=page, page_size=page_size, order_by=order_by, compute=compute,
    ), "search")


def llm_analysis(project_id, question, predicate_names=None, predicate_data=None,
                 params=None, prompt_tuning=None, prompt_tuning_name=None,
                 default_response=None, scope="user", compute=None):
    """Ask an LLM a question grounded in one or more predicate tables."""
    return _check(JarvisPyClient.llm_analysis(
        project_id=project_id, question=question, predicate_names=predicate_names,
        predicate_data=predicate_data, params=params, prompt_tuning=prompt_tuning,
        prompt_tuning_name=prompt_tuning_name, default_response=default_response,
        scope=scope, compute=compute,
    ), "llm analysis")


def download_concept(project_id, path=None, export_csv=False, concept_name=None,
                     scope="user", dest_path=None):
    """Download a project file, or export a concept to CSV and download it.

    Returns the local path the file was written to.
    """
    return JarvisPyClient.download_concept(
        project_id=project_id, path=path, export_csv=export_csv,
        concept_name=concept_name, scope=scope, dest_path=dest_path,
    )
