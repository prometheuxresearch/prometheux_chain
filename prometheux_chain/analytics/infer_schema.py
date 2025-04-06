import requests

from ..client.jarvispy_client import JarvisPyClient
from ..model.database import Database

"""
Schema Inference Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def infer_schema(database:Database, add_bind=True, add_model=False):
    try:
        response = JarvisPyClient.infer_schema(database, add_bind, add_model)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"