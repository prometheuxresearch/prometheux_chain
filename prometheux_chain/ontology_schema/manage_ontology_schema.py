"""
Ontology Schema Management Module

Save/load an ontology's schema definition, set concept schema roles, lineage
edits, and OWL import.

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"Ontology schema {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def save_ontology_schema(ontology_id, ontology_schema_data):
    """Save an ontology's schema definition."""
    response = JarvisPyClient.save_ontology_schema(
        ontology_id=ontology_id, ontology_schema_data=ontology_schema_data,
    )
    if response.get('status') != 'success':
        raise Exception(f"Ontology schema save failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def load_ontology_schema(ontology_id):
    """Load an ontology's schema definition (None if not set)."""
    return _check(JarvisPyClient.load_ontology_schema(ontology_id=ontology_id), "load")


def update_concept_ontology_schema_type(ontology_id, concept_name, ontology_schema_type=None,
                                        edge_source=None, edge_target=None):
    """Set a concept's schema role: 'node', 'edge' (with source/target), or reset."""
    return _check(JarvisPyClient.update_concept_ontology_schema_type(
        ontology_id=ontology_id, concept_name=concept_name, ontology_schema_type=ontology_schema_type,
        edge_source=edge_source, edge_target=edge_target,
    ), "update concept ontology schema type")


def add_to_lineage(ontology_id, element_type, element_data, all_nodes=None):
    """Add a single schema node or edge to the lineage."""
    return _check(JarvisPyClient.add_to_lineage(
        ontology_id=ontology_id, element_type=element_type, element_data=element_data,
        all_nodes=all_nodes,
    ), "add to lineage")


def import_owl(ontology_id, owl_content, base_namespace=None):
    """Import an OWL document and convert it to the schema-editor JSON format."""
    return _check(JarvisPyClient.import_owl(
        ontology_id=ontology_id, owl_content=owl_content, base_namespace=base_namespace,
    ), "import owl")
