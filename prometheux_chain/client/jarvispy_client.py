from ..config import config
import requests
import os

from ..data.database import Database

"""
JarvisPy Client Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


class JarvisPyClient:


    @staticmethod
    def cleanup_projects(workspace_id, project_id, project_scope):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/projects/{workspace_id}/cleanup"
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
    def save_project(workspace_id, project_id, project_name, project_scope):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/projects/{workspace_id}/save"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'id': project_id,
                'name': project_name,
                'scope': project_scope,
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def list_projects(workspace_id, project_scopes):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/projects/{workspace_id}/list"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'scopes': project_scopes
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def load_project(workspace_id, project_id, project_scope):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/projects/{workspace_id}/load"
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
    def cleanup_sources(workspace_id, source_ids):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/data/{workspace_id}/cleanup"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'source_ids': source_ids
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def connect_sources(workspace_id, database_payload: Database, compute_row_count=False):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/data/{workspace_id}/connect"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'database': database_payload.to_dict(),
            'computeRowCount': compute_row_count
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def list_sources(workspace_id):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/data/{workspace_id}/list"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'scope': 'user'
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
        return response.json()


    @staticmethod
    def cleanup_concepts(workspace_id, project_id, project_scope):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))
        
        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/concepts/{workspace_id}/{project_id}/cleanup"
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
    def save_concept(workspace_id, project_id, concept_logic, scope="user"):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/concepts/{workspace_id}/{project_id}/save"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'scope': scope,
            'concept_logic': concept_logic,
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def run_concept(
        workspace_id,
        project_id,
        concept_name,
        params=None,
        project_scope="user",
        step_by_step=False,
        materialize_intermediate_concepts=False,
        force_rerun=True,
        persist_outputs=False,
        python_scripts=None
    ):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/concepts/{workspace_id}/{project_id}/run"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'concept_name': concept_name,
            'params': params or {},
            'force_rerun': force_rerun,
            'persist_outputs': persist_outputs,
            'project_scope': project_scope,
            'step_by_step': step_by_step,
            'materialize_intermediate_concepts': materialize_intermediate_concepts
        }
        
        # Add python_scripts to payload if provided
        if python_scripts is not None:
            payload['python_scripts'] = python_scripts
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def list_concepts(workspace_id, project_id, project_scope):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/concepts/{workspace_id}/{project_id}/list"
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
    def save_kg(workspace_id, project_id, concepts, scope="user"):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/kgs/{workspace_id}/{project_id}/save"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'scope': scope
            },
            'virtual_kg': {
                'concepts': concepts
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def load_kg(workspace_id, project_id, scope="user"):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/kgs/{workspace_id}/{project_id}/load"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'scope': scope
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def graph_rag(
        workspace_id,
        project_id,
        question,
        graph=None,
        rag=None,
        llm=None,
        project_scope="user",
    ):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")

        url = f"{jarvispy_url}/api/v1/graphrag/{workspace_id}/{project_id}/query"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'question': question,
            'project_scope': project_scope
        }
        if graph:
            payload['graph'] = graph
        if rag:
            payload['rag'] = rag
        if llm:
            payload['llm'] = llm

        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    
    
    
    

    


















    # @staticmethod
    # def all_pairs_join(databases: list[Database], lhs_databases: list[Database], rhs_databases: list[Database], to_evaluate: bool, parallel: bool, output_type: str):
    #     jarvispy_url = config['JARVISPY_URL']
    #     pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

    # #     if not pmtx_token:
    # #         raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
    #     url = f"{jarvispy_url}/api/v1/all-pairs-join"
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'Authorization': f"Bearer {pmtx_token}"
    #     }
    #     payload = {
    #         "databasePayloads": [db.to_dict() for db in databases],
    #         "lhsDatabasePayloads": [db.to_dict() for db in lhs_databases],
    #         "rhsDatabasePayloads": [db.to_dict() for db in rhs_databases],
    #         "toEvaluate": to_evaluate,
    #         "parallel": parallel,
    #         "outputType": output_type
    #     }

    # #     response = requests.post(url, headers=headers, json=payload)
    # #     return response

    
    
    


    
    
    
    
    
    
    