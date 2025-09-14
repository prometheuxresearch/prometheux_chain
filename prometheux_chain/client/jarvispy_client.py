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
    def _handle_response(response):
        """
        Handle HTTP response and check for errors.
        Returns parsed JSON response or raises appropriate exception.
        """
        # Check HTTP status code first
        if response.status_code == 401:
            raise Exception("Unauthorized: Invalid or expired token. Please check your PMTX_TOKEN.")
        elif response.status_code == 403:
            raise Exception("Forbidden: You don't have permission to perform this action.")
        elif response.status_code == 404:
            raise Exception("Not Found: The requested resource was not found.")
        elif response.status_code >= 400:
            raise Exception(f"HTTP Error {response.status_code}: {response.text}")
        
        # Try to parse JSON response
        try:
            return response.json()
        except ValueError:
            raise Exception(f"Invalid JSON response from server: {response.text}")

    @staticmethod
    def export_workspace(workspace_id, scope="user"):
        """
        Export all tables from a workspace.
        
        Args:
            workspace_id (str): The ID of the workspace to export
            scope (str): The scope of the export (default: "user")
        
        Returns:
            dict: Response containing exported table data
        """
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/workspaces/{workspace_id}/export-tables"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'scope': scope
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return JarvisPyClient._handle_response(response)

    @staticmethod
    def import_workspace(export_data, workspace_id="workspace_id", scope="user"):
        """
        Import tables into a workspace from exported data.
        
        Args:
            export_data (dict): The complete export data from the export endpoint
            workspace_id (str): The ID of the target workspace (default: "workspace_id")
            scope (str): The target scope for the import (default: "user")
        
        Returns:
            dict: Response containing import status
        """
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/workspaces/import-tables"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'export_data': export_data,
            'workspace_id': workspace_id,
            'scope': scope
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return JarvisPyClient._handle_response(response)  

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
        return JarvisPyClient._handle_response(response)
    

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
        return JarvisPyClient._handle_response(response)


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
        return JarvisPyClient._handle_response(response)


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
        return JarvisPyClient._handle_response(response)


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
        return JarvisPyClient._handle_response(response)


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
        return JarvisPyClient._handle_response(response)


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
        return JarvisPyClient._handle_response(response)


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
        return JarvisPyClient._handle_response(response)


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
        return JarvisPyClient._handle_response(response)


    
    @staticmethod
    def save_concept(workspace_id, project_id, concept_logic, python_scripts, scope="user"):
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
            'python_scripts': python_scripts
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return JarvisPyClient._handle_response(response)


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
        persist_outputs=False
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
        
        response = requests.post(url, headers=headers, json=payload)
        return JarvisPyClient._handle_response(response)


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
        return JarvisPyClient._handle_response(response)


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
        return JarvisPyClient._handle_response(response)


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
        return JarvisPyClient._handle_response(response)


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
        return JarvisPyClient._handle_response(response)

    @staticmethod
    def copy_project(project_id, workspace_id, target_scope="user", new_project_name=None):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/projects/{workspace_id}/copy"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project_id': project_id,
            'workspace_id': workspace_id,
            'target_scope': target_scope,
            'new_project_name': new_project_name
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return JarvisPyClient._handle_response(response)

    