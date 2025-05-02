import time
import warnings

from ..client.jarvispy_client import JarvisPyClient
from ..common.vadalog_utils import process_vadalog_files

"""
Virtual Knowledge Graph Reasoning Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def reason(vadalog_file_paths, vadalog_params={}, measure_time=False, to_explain=False, to_persist=False, to_embed=False, scope="user"):
    # Check parameters compatibility
    if not to_explain and to_embed:
        warnings.warn("Embedding will be less effective if to_explain is set to False.")

    # Process vadalog files into the structured format
    vadalog_programs = process_vadalog_files(vadalog_file_paths)

    # Measure time if needed
    start_time = time.time() if measure_time else None

    # Call JarvisPyClient
    response = JarvisPyClient.reason(
        vadalog_programs=vadalog_programs,
        vadalog_params=vadalog_params,
        to_explain=to_explain,
        to_persist=to_persist,
        to_embed=to_embed,
        scope=scope
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
