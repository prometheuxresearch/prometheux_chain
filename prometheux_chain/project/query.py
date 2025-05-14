import os
from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Virtual Knowledge Graph Query Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def query(virtual_kg, file_path_or_query: str, params=None):
    if params is None:
        params = {}
    if virtual_kg is None:
        raise Exception("Virtual Knowledge Graph is null. Cannot perform query.")

    # Check if the query is a string or a file path
    language_type, query_read = _parse_input(file_path_or_query)

    # Call JarvisPyClient query
    response = JarvisPyClient.query(
        virtual_kg=virtual_kg,
        query=query_read,
        params=params,
        language_type=language_type
    )

    # Handle response codes
    response_json = response.json()

    if response.status_code not in (200, 504):
        msg = response_json.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during querying: {msg}")

    if response.status_code == 504:
        evaluation_response = {}
    else:
        evaluation_response = response_json.get("data", {}).get('resultSet', {})

    facts = []
    for result_set_key, result_set_values in evaluation_response.items():
        for value in result_set_values:
            facts.append(f"{result_set_key}({', '.join(str(item) for item in value)})")

    return facts


def _parse_input(file_path_or_query: str):
    """
    Distinguish whether `file_path_or_query` is:
      - A Datalog query (starts with '?-')
      - A SQL query (starts with 'select')
      - A file path ending with .vada or .sql
        (and must exist)

    Returns:
        (query_type, content)
        where query_type is one of {"datalog", "sql", ".vada", ".sql"}
        and content is the original string.

    Raises:
        ValueError: If none of the criteria are satisfied or the file doesn't exist.
    """
    trimmed = file_path_or_query.strip()
    lower_trimmed = trimmed.lower()

    # Check for Datalog query
    if lower_trimmed.startswith('?-') or ':-' in lower_trimmed:
        return "vadalog", trimmed

    # Check for SQL query
    if lower_trimmed.startswith('select'):
        return "sql", trimmed

    # 3) Otherwise, treat it as a file path ending with .vada or .sql
    valid_extensions = ['.vada', '.sql']
    ext = None
    for extension in valid_extensions:
        if lower_trimmed.endswith(extension):
            ext = extension.replace(".", "")
            if ext == "vada":
                ext = "vadalog"
            break

    if not ext:
        raise ValueError(
            f"File path must end with one of {valid_extensions}, but got: {file_path_or_query}"
        )

    # Check if the file actually exists
    if not os.path.exists(trimmed):
        raise FileNotFoundError(
            f"File does not exist: {trimmed}"
        )

    try:
        with open(trimmed, 'r') as file:
            vadalog_or_sql_query = file.read()
    except IOError as e:
        raise Exception(f"Error opening file {trimmed}: {e}")

    # If we get here, it's a valid file path with extension .vada or .sql
    return ext, vadalog_or_sql_query
