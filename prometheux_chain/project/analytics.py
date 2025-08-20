import requests
from ..client.jarvispy_client import JarvisPyClient
from ..data.database import Database


"""
Analytics Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def infer_schema(database:Database, add_bind=True, add_model=False):
    try:
        response = JarvisPyClient.infer_schema(database, add_bind, add_model)
        if response.status_code == 200:
            return response.json()['data']
        else:
            message = response.json().get('message', response)
            return f"Error: Received status code {response.status_code} with error {message}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


def all_pairs_join(databases : list[Database], to_evaluate: bool=True, parallel: bool=False):
    try:
        response = JarvisPyClient.all_pairs_join(databases, to_evaluate, parallel)
        if response.status_code == 200:
           return response.json()['data']
        else:
            message = response.json().get('message', response)
            return f"Error: Received status code {response.status_code} with error {message}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    

