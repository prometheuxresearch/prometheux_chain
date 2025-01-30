import time
import os
from ..client.jarvispy_client import JarvisPyClient
from typing import Dict

"""
Virtual Knowledge Graph Reasoning and Querying Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def reason(vada_file_paths, params=None, measure_time=False, to_explain=False, to_persist=False):
    # Check if JarvisPy is reachable
    if not JarvisPyClient.is_reachable():
        print("Error: JarvisPy backend is not reachable.")
        return None

    if params is None:
        params = {}

    # Build the ontologiesPaths from vada_file_paths
    ontologiesPaths = []
    if isinstance(vada_file_paths, str):
        ontologiesPaths = [[vada_file_paths]]
    elif isinstance(vada_file_paths, list):
        for ontologyPaths in vada_file_paths:
            if isinstance(ontologyPaths, str):
                ontologiesPaths.append([ontologyPaths])
            elif isinstance(ontologyPaths, list):
                ontologiesPaths.append(ontologyPaths)

    # Check that there are no .vada files with the same name
    all_filenames = []
    for path_group in ontologiesPaths:
        for path in path_group:
            filename = os.path.basename(path)
            all_filenames.append(filename)
    duplicates = set([f for f in all_filenames if all_filenames.count(f) > 1])
    if duplicates:
        raise Exception(f"Duplicate .vada filenames found: {', '.join(duplicates)}")

    # Read .vada files and store in a list of lists of dict <file_name, file_content>
    vadalog_programs = []
    for ontologiesPath in ontologiesPaths:
        vadalog_programs_serial_evaluation: list[Dict[str:str]] = []
        for ontologyPath in ontologiesPath:
            try:
                with open(ontologyPath, 'r') as file:
                    file_content = file.read()
                    filename = os.path.basename(ontologyPath)
                    vadalog_program_single = {filename: file_content}
                    vadalog_programs_serial_evaluation.append(vadalog_program_single)
            except IOError as e:
                raise Exception(f"Error opening file {ontologyPath}: {e}")
        vadalog_programs.append(vadalog_programs_serial_evaluation)

    # Measure time if needed
    start_time = time.time() if measure_time else None

    # Call JarvisPyClient
    response = JarvisPyClient.reason(
        programs=vadalog_programs,
        params=params,
        to_explain=to_explain,
        to_persist=to_persist
    )

    # Handle response codes
    if response.status_code not in (200, 504):
        msg = response.json().get('message', 'Unknown error')
        raise Exception(f"An exception occurred during reasoning: {msg}")

    if response.status_code == 504:
        virtual_knowledge_graph = None

    else:  # response.status_code == 200
        virtual_knowledge_graph = response.json()['data']

    # Print timing info if needed
    if measure_time:
        elapsed_time = time.time() - start_time
        print(f"Virtual Knowledge Graph reasoning completed in {elapsed_time:.2f} seconds.")

    return virtual_knowledge_graph


def query(virtual_kg, file_path_or_query: str, params=None):
    # Check if JarvisPy is reachable
    if not JarvisPyClient.is_reachable():
        print("Error: JarvisPy backend is not reachable.")
        return None

    if params is None:
        params = {}
    if virtual_kg is None:
        raise Exception("Virtual Knowledge Graph is null. Cannot perform query.")

    # Check if the query is a string or a file path
    language_type, query_read = __parse_input(file_path_or_query)

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
        evaluation_response = response_json.get("data", {})

    return evaluation_response.get("query_results", [])


def __parse_input(file_path_or_query: str):
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
