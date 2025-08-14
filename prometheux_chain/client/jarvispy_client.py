from ..config import config
import requests
import os

from ..model.database import Database

"""
JarvisPy Client Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


class JarvisPyClient:


    @staticmethod
    def cleanup_projects(project_id, project_scope):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/projects/cleanup"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'id': project_id,
                'scope': project_scope
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    

    @staticmethod
    def save_project(project_id, project_name, project_scope, to_persist):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/projects/save"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'id': project_id,
                'name': project_name,
                'scope': project_scope,
                'to_persist': to_persist
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def list_projects(scope="user"):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/projects/list"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'scopes': [scope]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    @staticmethod
    def load_project(project_id, scope="user"):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/projects/load"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'id': project_id,
                'scope': scope
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def cleanup_sources(project_id, project_scope, source_ids):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/data/{project_id}/cleanup"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'scope': project_scope
            },
            'source_ids': source_ids
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def connect_sources(project_id, project_scope, database_payload: Database, add_model=False):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/data/{project_id}/connect"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'scope': project_scope
            },
            'database': database_payload.to_dict(),
            'addModel': add_model
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    
    @staticmethod
    def list_sources(project_id, project_scope):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/data/{project_id}/list"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'scope': project_scope
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    

    @staticmethod
    def list_concepts(project_id, project_scope):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/concepts/{project_id}/list"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'scope': project_scope
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    

    @staticmethod
    def overview_concepts(project_id, project_scope):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/concepts/{project_id}/overview"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        
        payload = {
            'project': {
                'scope': project_scope
            },
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    
    
    @staticmethod
    def cleanup_kgs(project_id, project_scope, kg_ids):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in env variables or config.")

        url = f"{jarvispy_url}/api/v1/kgs/{project_id}/cleanup"
        payload = {
            'project': {
                'scope': project_scope
            },
            'kg_ids': kg_ids
        }
        headers = {
            'Authorization': f"Bearer {pmtx_token}",
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    
        
    
    

    
















    @staticmethod
    def infer_schema(database : Database, add_bind: bool, add_model: bool):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/data/infer-schema"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            "database": database.to_dict(),
            "addBind": add_bind,
            "addModel": add_model
        }
        response = requests.post(url, headers=headers, json=payload)
        return response


    @staticmethod
    def all_pairs_join(databases: list[Database], lhs_databases: list[Database], rhs_databases: list[Database], to_evaluate: bool, parallel: bool, output_type: str):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

    #     if not pmtx_token:
    #         raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/all-pairs-join"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            "databasePayloads": [db.to_dict() for db in databases],
            "lhsDatabasePayloads": [db.to_dict() for db in lhs_databases],
            "rhsDatabasePayloads": [db.to_dict() for db in rhs_databases],
            "toEvaluate": to_evaluate,
            "parallel": parallel,
            "outputType": output_type
        }

    #     response = requests.post(url, headers=headers, json=payload)
    #     return response
    


    
    
    
    
    
    
    