import os

from prometheux_chain.client.jarvispy_client import JarvisPyClient
from prometheux_chain.common.vadalog_utils import read_vadalog_file

"""
Compile Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

def compile(vadalog_file_path: str):
    """
    Compiles a .vada file using JarvisPyClient.
    Returns "OK" on success, or raises RuntimeError on failure.
    """
    # 1) Check reachability
    if not JarvisPyClient.is_reachable():
        raise RuntimeError("JarvisPy backend is not reachable.")

    # 2) Validate file existence
    if not os.path.exists(vadalog_file_path):
        raise FileNotFoundError(f"The file {vadalog_file_path} does not exist.")

    # 3) Validate extension
    if not vadalog_file_path.endswith(".vada"):
        raise ValueError("The file must have a .vada extension.")

    # 4) Read the Vadalog file
    vadalog_program = read_vadalog_file(vadalog_file_path)

    # 5) Call JarvisPyClient compile
    #    (This will raise a RuntimeError if something goes wrong)
    response_json = JarvisPyClient.compile(vadalog_program)

    # 6) If we get here, it's a success
    #    "response_json" might contain additional data from the server
    return "OK"