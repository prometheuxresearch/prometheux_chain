import requests

from ..client.jarvispy_client import JarvisPyClient
from ..model.database import Database

"""
All Pairs Join Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def all_pairs_join(databases : list[Database], to_evaluate: bool=True, parallel: bool=False):
    try:
        response = JarvisPyClient.all_pairs_join(databases, to_evaluate, parallel)
        if response.status_code == 200:
           return response.json()['data']
        else:
            return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
