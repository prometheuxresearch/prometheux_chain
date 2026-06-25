"""
Ontology Management Module

Save/load project ontologies, set concept ontology roles, lineage edits,
description generation, and OWL import.

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"Ontology {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def save_ontology(project_id, ontology_data, scope="user"):
    """Save a project's ontology definition."""
    response = JarvisPyClient.save_ontology(
        project_id=project_id, ontology_data=ontology_data, scope=scope,
    )
    if response.get('status') != 'success':
        raise Exception(f"Ontology save failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def load_ontology(project_id, scope="user"):
    """Load a project's ontology definition (None if not set)."""
    return _check(JarvisPyClient.load_ontology(project_id=project_id, scope=scope), "load")


def update_concept_ontology_type(project_id, concept_name, ontology_type=None,
                                 edge_source=None, edge_target=None, scope="user"):
    """Set a concept's ontology role: 'node', 'edge' (with source/target), or reset."""
    return _check(JarvisPyClient.update_concept_ontology_type(
        project_id=project_id, concept_name=concept_name, ontology_type=ontology_type,
        edge_source=edge_source, edge_target=edge_target, scope=scope,
    ), "update concept ontology type")


def add_to_lineage(project_id, element_type, element_data, all_nodes=None, scope="user"):
    """Add a single ontology node or edge to the lineage."""
    return _check(JarvisPyClient.add_to_lineage(
        project_id=project_id, element_type=element_type, element_data=element_data,
        all_nodes=all_nodes, scope=scope,
    ), "add to lineage")


def describe_ontology(project_id, ontology_data, scope="user"):
    """Generate a natural-language description of a project's ontology."""
    return _check(JarvisPyClient.describe_ontology(
        project_id=project_id, ontology_data=ontology_data, scope=scope,
    ), "describe")


def import_owl(project_id, owl_content, base_namespace=None):
    """Import an OWL document and convert it to the ontology-editor JSON format."""
    return _check(JarvisPyClient.import_owl(
        project_id=project_id, owl_content=owl_content, base_namespace=base_namespace,
    ), "import owl")
