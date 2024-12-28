import time
import os
from .Fact import Fact
from ..client.JarvisPyClient import JarvisPyClient
from typing import Dict


def reason(vada_file_paths, params={}, measure_time=False, to_explain=False, to_persist=False):
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
        vadalog_programs_serial_evaluation:list[Dict[str:str]] = []
        for ontologyPath in ontologiesPath:
            try:
                with open(ontologyPath, 'r') as file:
                    file_content = file.read()
                    filename = os.path.basename(ontologyPath)
                    vadalog_program_single = {}
                    vadalog_program_single[filename] = file_content
                    vadalog_programs_serial_evaluation.append(vadalog_program_single)
            except IOError as e:
                raise Exception(f"Error opening file {ontologyPath}: {e}")
        vadalog_programs.append(vadalog_programs_serial_evaluation)

    # Measure time if needed
    start_time = time.time() if measure_time else None
    # Call JarvisPyClient
    response = JarvisPyClient.reason(
        vada_programs=vadalog_programs,
        vada_params=params,
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

def query(virtual_kg, vada_file_path, params={}):
    if virtual_kg is None:
        raise Exception("Virtual Knowledge Graph is null. Cannot perform query.")

    # Read the .vada file
    try:
        with open(vada_file_path, 'r') as file:
            vadalog_program = file.read()
    except IOError as e:
        raise Exception(f"Error opening file {vada_file_path}: {e}")

    # Call JarvisPyClient query
    response = JarvisPyClient.query(virtual_kg, vadalog_program, params)

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