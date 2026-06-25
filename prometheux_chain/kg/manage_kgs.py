"""
KG Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

from ..client.jarvispy_client import JarvisPyClient


def _check(response, action="operation"):
    """Raise on error, return data on success."""
    if response.get('status') != 'success':
        raise Exception(f"KG {action} failed: {response.get('message', 'Unknown error')}")
    return response.get('data')


def visualize_concept_lineage(project_id, scope="user"):
    """Return concept-level lineage (nodes + transitive dependency edges)."""
    return _check(JarvisPyClient.visualize_concept_lineage(
        project_id=project_id, scope=scope,
    ), "visualize concept lineage")


def build_graph(project_id, output_predicate, column_roles, scope="user", page=1,
                page_size=0, order_by=None, pagination_mode="records", max_depth=50,
                source_node=None, target_node=None, recompute=False, compute=None):
    """Build a graph visualization from an edge predicate's output facts.

    ``column_roles`` must contain integer ``source`` and ``target`` positions
    (and optionally ``edge_value``).
    """
    return _check(JarvisPyClient.build_graph(
        project_id=project_id, output_predicate=output_predicate, column_roles=column_roles,
        scope=scope, page=page, page_size=page_size, order_by=order_by,
        pagination_mode=pagination_mode, max_depth=max_depth, source_node=source_node,
        target_node=target_node, recompute=recompute, compute=compute,
    ), "build graph")


def list_graph_functions():
    """List the available graph analytics functions and their parameter schemas."""
    return _check(JarvisPyClient.list_graph_functions(), "list graph functions")


def run_graph_analytics(project_id, output_predicate, column_roles, function,
                        function_params=None, scope="user", compute=None):
    """Run a graph analytics function (e.g. pagerank, cc, dc, paths) over an edge predicate."""
    return _check(JarvisPyClient.run_graph_analytics(
        project_id=project_id, output_predicate=output_predicate, column_roles=column_roles,
        function=function, function_params=function_params, scope=scope, compute=compute,
    ), "run graph analytics")
