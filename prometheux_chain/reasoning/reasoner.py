import time
import os
from .Fact import Fact
from ..client.JarvisPyClient import JarvisPyClient


class Reasoner:

    @staticmethod
    def reason(vada_file_paths, params=None, measure_time=False, to_explain=False, to_materialize=False):
        # Preprocess parameters (quote string parameters)
        if params is None:
            params = {}
        for k in params:
            if isinstance(params[k], str):
                params[k] = f'"{params[k]}"'

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

        # Read .vada files and store in a list of lists of pairs <file_name, file_content>
        vadalog_programs = []
        for ontologiesPath in ontologiesPaths:
            vadalog_programs_single = []
            for ontologyPath in ontologiesPath:
                try:
                    with open(ontologyPath, 'r') as file:
                        file_content = file.read()
                        vadalog_programs_single.append((ontologyPath, file_content))
                except IOError as e:
                    raise Exception(f"Error opening file {ontologyPath}: {e}")
            vadalog_programs.append(vadalog_programs_single)

        # Measure time if needed
        start_time = time.time() if measure_time else None

        # Call JarvisPyClient
        response = JarvisPyClient.reason(
            vada_programs=vadalog_programs,
            vada_params=params,
            to_explain=to_explain,
            to_materialize=to_materialize
        )

        # Handle response codes
        if response.status_code not in (200, 504):
            msg = response.json().get('message', 'Unknown error')
            raise Exception(f"An exception occurred during reasoning: {msg}")

        if response.status_code == 504:
            virtual_knowledge_graph = None

        else:  # response.status_code == 200
            virtual_knowledge_graph = response.json()

        # Print timing info if needed
        if measure_time:
            elapsed_time = time.time() - start_time
            print(f"Virtual Knowledge Graph reasoning completed in {elapsed_time:.2f} seconds.")

        return virtual_knowledge_graph

    @staticmethod
    def query(virtual_kg, vada_file_path, params=None):
        if params is None:
            params = {}
        if virtual_kg is None:
            raise Exception("Virtual Knowledge Graph is null. Cannot perform query.")

        # Preprocess parameters (quote string parameters)
        for k in params:
            if isinstance(params[k], str):
                params[k] = f'"{params[k]}"'

        # Read the .vada file
        try:
            with open(vada_file_path, 'r') as file:
                vadalog_program = file.read()
        except IOError as e:
            raise Exception(f"Error opening file {vada_file_path}: {e}")

        # Call JarvisPyClient query
        response = JarvisPyClient.query(vadalog_program, params, virtual_kg)

        # Handle response codes
        if response.status_code not in (200, 504):
            msg = response.json().get('message', 'Unknown error')
            raise Exception(f"An exception occurred during querying: {msg}")

        if response.status_code == 504:
            evaluation_response = {}
        else:
            evaluation_response = response.json().get("data", {})

        output_facts = []
        for predicate_name, arguments_list in evaluation_response.get('resultSet', {}).items():
            types = evaluation_response.get('types', {}).get(predicate_name, [])
            column_names = evaluation_response.get('columnNames', {}).get(predicate_name, [])
            for arguments in arguments_list:
                fact = Fact(predicate_name, arguments, column_names, types)
                output_facts.append(fact)

        return output_facts
