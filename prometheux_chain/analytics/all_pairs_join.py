import requests

from ..client.jarvispy_client import JarvisPyClient
from ..model.database import Database

"""
All Pairs Join Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def all_pairs_join(databases : list[Database], lhs_databases : list[Database], rhs_databases : list[Database], to_evaluate: bool=True, parallel: bool=False, output_type:str="structured"):
    # is it possible to have either databases or (lhs_databases and rhs_databases)
    if not databases or len(databases) == 0:
        lhs_databases = []
        rhs_databases = []
    elif (not lhs_databases or len(lhs_databases) == 0) and (not rhs_databases or len(rhs_databases) == 0):
        raise ValueError("if databases is not provided, lhs_databases and rhs_databases must be provided")
    else:
        raise ValueError("At least one of databases or (lhs_databases and rhs_databases must be provided)")
    try:
        response = JarvisPyClient.all_pairs_join(databases, lhs_databases, rhs_databases, to_evaluate, parallel, output_type)
        if response.status_code == 200:
           return response.json()['data']
        else:
            return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
