import os
from typing import List, Dict

"""
Vadalog Utility Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def process_vadalog_files(vada_file_paths):
    """
    Process Vadalog (.vada) files and structure them in a list of lists of dicts
    with {file_name: file_content} while ensuring uniqueness.

    Parameters:
        vada_file_paths (str or list): Path(s) to the .vada files.

    Returns:
        list: Processed vadalog program structure.

    Raises:
        Exception: If duplicate .vada filenames are found or if files cannot be read.
    """

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
        vadalog_programs_serial_evaluation: List[Dict[str, str]] = []
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

    return vadalog_programs
