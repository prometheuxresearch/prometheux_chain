from ..client.jarvispy_client import JarvisPyClient

"""
Knowledge Graph Explanation Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def explain(virtual_kg, fact_to_explain):
    if virtual_kg is None:
        raise Exception("Virtual Knowledge Graph is null. Cannot perform explanation.")

    if not virtual_kg['to_explain']:
        raise Exception("No facts to explain. Cannot perform explanation.")

    if not fact_to_explain:
        raise Exception("Fact to explain is null or empty. Cannot perform explanation.")

    response = JarvisPyClient.explain(virtual_kg, fact_to_explain)

    # Handle response codes
    if response.status_code not in (200, 504):
        msg = response.json().get('message', 'Unknown error')
        raise Exception(f"An exception occurred during explanation: {msg}")

    if response.status_code == 504:
        explanation = None
    else:  # status_code == 200
        explanation = response.json().get("data", {})

    return explanation
