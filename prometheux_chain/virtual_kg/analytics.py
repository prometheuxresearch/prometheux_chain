import requests
from ..client.jarvispy_client import JarvisPyClient
from ..model.database import Database


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
            return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


def all_pairs_join(databases : list[Database], to_evaluate: bool=True, parallel: bool=False):
    try:
        response = JarvisPyClient.all_pairs_join(databases, to_evaluate, parallel)
        if response.status_code == 200:
           return response.json()['data']
        else:
            return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    

def kg_overview(virtual_kg):
    if not virtual_kg:
        raise ValueError("Missing 'virtual_kg' parameter")
    
    return JarvisPyClient.kg_overview(virtual_kg)


def connect_kg_sources(virtual_kg, database_payload, add_model=False):
    try:
        response = JarvisPyClient.connect_kg_sources(virtual_kg, database_payload, add_model)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


def load_kg_sources(virtual_kg):
    try:
        response = JarvisPyClient.load_kg_sources(virtual_kg)
        if response.status_code == 200:
            return response.json()['data']
        else:
            return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


def cleanup_kg_sources(virtual_kg, source_ids=None):
    try:
        response = JarvisPyClient.cleanup_kg_sources(virtual_kg, source_ids)
        if response.status_code == 200:
            return True
        else:
            return f"Error: Received status code {response.status_code} with error {response.json()['message']}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"