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
    def save_project(project_id, project_scope, to_persist):
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
    def cleanup_notebooks(project_id, project_scope, notebook_ids=None):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/notebooks/{project_id}/cleanup"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'scope': project_scope
            },
            'notebook_ids': notebook_ids
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    

    @staticmethod
    def save_notebook(project_id, project_scope, notebook_id, notebook_name):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/notebooks/{project_id}/save"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'scope': project_scope
            },
            'notebook': {
                'id': notebook_id,
                'name': notebook_name
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    

    @staticmethod
    def list_notebooks(project_id, project_scope):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/notebooks/{project_id}/list"
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
    def load_notebook(project_id, notebook_id, project_scope):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/notebooks/{project_id}/load"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'scope': project_scope
            },
            'notebook': {
                'id': notebook_id
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def cleanup_cells(project_id, project_scope, notebook_id, cell_ids=None):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/notebooks/{project_id}/{notebook_id}/cleanup-cells"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'scope': project_scope
            },
            'cell_ids': cell_ids
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    
    
    @staticmethod
    def save_cell(project_id, project_scope, notebook_id, cell_content, cell_position, cell_id=None):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/notebooks/{project_id}/{notebook_id}/save-cell"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        
        payload = {
            'project': {
                'scope': project_scope
            },
            'cell': {
                'notebook_id': notebook_id,
                'id': cell_id,
                'content': cell_content,
                'position': cell_position
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

    
    @staticmethod
    def run_cell(project_id, notebook_id, project_scope, cell_content, cell_position, cell_id=None):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/notebooks/{project_id}/{notebook_id}/run-cell"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'project': {
                'scope': project_scope
            },
            'cell': {
                'notebook_id': notebook_id,
                'content': cell_content,
                'position': cell_position,
                'id': cell_id
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def list_cells(project_id, project_scope, notebook_id):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/notebooks/{project_id}/{notebook_id}/list-cells"
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
    def save_kg(virtual_kg):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in env variables or config.")
        
        url = f"{jarvispy_url}/api/v1/save-kg"
        payload = {
            'virtual_kg': virtual_kg
        }
        headers = {
            'Authorization': f"Bearer {pmtx_token}",
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload)
        return response


    @staticmethod
    def list_kgs(scopes):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in env variables or config.")
        
        url = f"{jarvispy_url}/api/v1/list-kgs"
        payload = {
            'scopes': scopes
        }
        headers = {
            'Authorization': f"Bearer {pmtx_token}",
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return response.json()


    @staticmethod
    def load_kg(virtual_kg):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in env variables or config.")
        
        url = f"{jarvispy_url}/api/v1/load-kg"
        payload = {
            'virtual_kg': virtual_kg,
        }
        headers = {
            'Authorization': f"Bearer {pmtx_token}",
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    

    @staticmethod
    def save_kg_chat(virtual_kg, prompt, response):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/save-kg-chat"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        
        payload = {
            'virtual_kg': virtual_kg,
            'chat': {
                'prompt': prompt,
                'response': response
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def load_kg_chat(virtual_kg):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/load-kg-chat"
        payload = {
            'virtual_kg': virtual_kg
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def cleanup_kg_chat(virtual_kg, chat_ids=None):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/cleanup-kg-chat"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        
        payload = {
            'virtual_kg': virtual_kg,
            'chat_ids': chat_ids
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response


    @staticmethod   
    def save_kg_query(virtual_kg, query_id, query_logic):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in env variables or config.")

        url = f"{jarvispy_url}/api/v1/save-kg-query"
        payload = {
            'virtual_kg': virtual_kg,
            'query': {
                'query_id': query_id,
                'query_logic': query_logic,
            }
        }
        headers = {
            'Authorization': f"Bearer {pmtx_token}",
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    

    @staticmethod
    def load_kg_queries(virtual_kg):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in env variables or config.")

        url = f"{jarvispy_url}/api/v1/load-kg-queries"
        payload = {
            'virtual_kg': virtual_kg,
        }
        headers = {
            'Authorization': f"Bearer {pmtx_token}",
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
    

    @staticmethod
    def cleanup_kg_queries(virtual_kg, query_ids):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in env variables or config.")

        url = f"{jarvispy_url}/api/v1/cleanup-kg-queries"
        payload = {
            'virtual_kg': virtual_kg,
            'query_ids': query_ids
        }
        headers = {
            'Authorization': f"Bearer {pmtx_token}",
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=payload)
        return response
 

    @staticmethod
    def compile(ontology):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN'))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        url = f"{jarvispy_url}/api/v1/compile"
        payload = {'ontology': ontology}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            try:
                response_json = response.json()
                error_msg = response_json.get("message", "Unknown error from backend.")
            except Exception:
                error_msg = response.text or "Unknown error from backend."
            raise RuntimeError(f"Compilation failed (HTTP {response.status_code}). {error_msg}")

        try:
            response_json = response.json()
        except Exception as e:
            raise RuntimeError(f"Failed to parse JSON response from JarvisPy backend: {str(e)}")

        if response_json.get("status") == "error":
            error_msg = response_json.get("message", "Unknown error from backend.")
            raise RuntimeError(f"Compilation failed: {error_msg}")

        return response_json
    

    @staticmethod
    def reason(vadalog_programs, vadalog_params, to_explain, to_persist, to_embed, scope):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN'))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        url = f"{jarvispy_url}/api/v1/reason"
        payload = {
            'vadalog_programs': vadalog_programs,
            'vadalog_params': vadalog_params,
            'to_explain': to_explain,
            'to_persist': to_persist,
            'to_embed': to_embed,
            'embedding_config': {
                'embedding_provider': config.get("EMBEDDING_PROVIDER"),
                'embedding_api_key': config.get("EMBEDDING_API_KEY"),
                'embedding_version': config.get("EMBEDDING_VERSION"),
                'embedding_dimensions': config.get("EMBEDDING_DIMENSIONS"),
                'azure_embedding_endpoint': config.get("AZURE_EMBEDDING_ENDPOINT"),
                'azure_embedding_api_version': config.get("AZURE_EMBEDDING_API_VERSION")
            },
            'scope': scope
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response
    

    @staticmethod
    def kg_overview(virtual_kg):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/kg-overview"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        
        payload = {
            'virtual_kg': virtual_kg
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()


    @staticmethod
    def query(virtual_kg, query, params, language_type):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        url = f"{jarvispy_url}/api/v1/query"
        payload = {
            'virtual_kg': virtual_kg,
            'query': query,
            'params': params,
            'language_type': language_type
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response


    @staticmethod
    def explain(virtual_kg, fact_to_explain):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        url = f"{jarvispy_url}/api/v1/explain"
        payload = {
            'fact_to_explain': fact_to_explain,
            'virtual_kg': virtual_kg
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response


    @staticmethod
    def visualize_predicate_graph(vadalog_program: str):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))
        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        url = f"{jarvispy_url}/api/v1/visualize/predicate-graph"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'vadalog_program': vadalog_program
        }
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    

    @staticmethod
    def visualize_kg_schema(vadalog_program: str):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))
        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        url = f"{jarvispy_url}/api/v1/visualize/kg-schema"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'vadalog_program': vadalog_program
        }
        response = requests.post(url, json=payload, headers=headers)    
        return response.json()


    @staticmethod
    def validate(text, guardrail_program):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")

        url = f"{jarvispy_url}/api/v1/validate"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'text': text,
            'guardrail_program': guardrail_program,
            'llm_config': {
                'llm_provider': config.get("LLM_PROVIDER"),
                'llm_api_key': config.get("LLM_API_KEY"),
                'llm_version': config.get("LLM_VERSION"),
                'llm_temperature': config.get("LLM_TEMPERATURE"),
                'llm_max_tokens': config.get("LLM_MAX_TOKENS"),
                'azure_llm_endpoint': config.get("AZURE_LLM_ENDPOINT"),
                'azure_llm_api_version': config.get("AZURE_LLM_API_VERSION")
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        return response


    @staticmethod
    def rag(question, virtual_kg, to_explain):
        if not question and not virtual_kg:
            raise Exception("Please provide a question to ask and a virtual knowledge graph")

        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")

        url = f"{jarvispy_url}/api/v1/rag"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'question': question,
            'virtual_kg': virtual_kg,
            'to_explain': to_explain,
            'embedding_config': {
                'embedding_provider': config.get("EMBEDDING_PROVIDER"),
                'embedding_api_key': config.get("EMBEDDING_API_KEY"),
                'embedding_model_version': config.get("EMBEDDING_VERSION"),
                'embedding_dimensions': config.get("EMBEDDING_DIMENSIONS"),
                'azure_embedding_endpoint': config.get("AZURE_EMBEDDING_ENDPOINT"),
                'azure_embedding_api_version': config.get("AZURE_EMBEDDING_API_VERSION")
            }
        }
        response = requests.post(url, headers=headers, json=payload)
        return response
    
    
    @staticmethod
    def chat(question = None, facts_and_explanations = None, translated_question_rules = None, top_retrieved_facts = None, predicates_and_models = None, to_explain = None, stream = False):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
                
        if stream:
            url = f"{jarvispy_url}/api/v1/chat/stream"
        else:
            url = f"{jarvispy_url}/api/v1/chat"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            "question": question,
            "facts_and_explanations": facts_and_explanations,
            "translated_question_rules": translated_question_rules,
            "top_retrieved_facts": top_retrieved_facts,
            "predicates_and_models": predicates_and_models,
            "to_explain": to_explain,
            "llm_config": {
                "llm_provider": config.get("LLM_PROVIDER"),
                "llm_api_key": config.get("LLM_API_KEY"),
                "llm_version": config.get("LLM_VERSION"),
                "llm_temperature": config.get("LLM_TEMPERATURE"),
                "llm_max_tokens": config.get("LLM_MAX_TOKENS")
            }
        }

        response = requests.post(url, headers=headers, json=payload)
        return response
    

    @staticmethod
    def translate(domain_knowledge):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/translate_nl_to_vadalog"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            "domain_knowledge": domain_knowledge,
        }
        response = requests.post(url, headers=headers, json=payload)
        return response


    @staticmethod
    def translate_from_rdf(rdf_data):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{jarvispy_url}/api/v1/translate_rdf_to_vadalog"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'rdf_data': rdf_data
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response


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
            "database_payload": database.to_dict(),
            "addBind": add_bind,
            "addModel": add_model
        }
        response = requests.post(url, headers=headers, json=payload)
        return response


    @staticmethod
    def all_pairs_join(databases: list[Database], lhs_databases: list[Database], rhs_databases: list[Database], to_evaluate: bool, parallel: bool, output_type: str):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
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

        response = requests.post(url, headers=headers, json=payload)
        return response
    


    
    
    
    
    
    
    