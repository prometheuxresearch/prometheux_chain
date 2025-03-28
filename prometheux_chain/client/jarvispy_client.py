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
    def cleanup(virtual_kg=None):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in env variables or config.")

        url = f"{jarvispy_url}/api/v1/cleanup"
        headers = {
            'Authorization': f"Bearer {pmtx_token}",
            'Content-Type': 'application/json'
        }
        if virtual_kg:
            response = requests.post(url, headers=headers, json=virtual_kg)
        else:
            response = requests.post(url, headers=headers)
        return response
    
    @staticmethod
    def save(virtual_kg):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in env variables or config.")
        
        url = f"{jarvispy_url}/api/v1/save-kg"
        headers = {
            'Authorization': f"Bearer {pmtx_token}",
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=virtual_kg)
        return response

    @staticmethod
    def list_kgs():
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in env variables or config.")
        
        url = f"{jarvispy_url}/api/v1/list-kgs"
        headers = {
            'Authorization': f"Bearer {pmtx_token}",
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        return response.json()

    @staticmethod
    def load(kg_id):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in env variables or config.")
        
        url = f"{jarvispy_url}/api/v1/load-kg"
        headers = {
            'Authorization': f"Bearer {pmtx_token}",
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, json=kg_id)
        return response.json()
    
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
    def reason(vadalog_programs, vadalog_params, to_explain, to_persist, to_embed):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN'))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")
        
        # Additional LLM-related config
        llm_api_key = None
        embedding_model_version = None
        embedding_dimensions = None

        url = f"{jarvispy_url}/api/v1/reason"
        payload = {
            'vadalog_programs': vadalog_programs,
            'vadalog_params': vadalog_params,
            'to_explain': to_explain,
            'to_persist': to_persist,
            'to_embed': to_embed,
            'embedding_api_key': llm_api_key,
            'embedding_model_version': embedding_model_version,
            'embedding_dimensions': embedding_dimensions
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response

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

        # Additional LLM-related config
        llm_api_key = config.get('LLM_API_KEY', None)
        llm_version = config.get('LLM_VERSION', 'gpt-4o')
        llm_temperature = config.get('LLM_TEMPERATURE', 0.50)
        llm_max_tokens = config.get('LLM_MAX_TOKENS', 2000)

        url = f"{jarvispy_url}/api/v1/validate"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'text': text,
            'guardrail_program': guardrail_program,
            'llm_api_key': llm_api_key,
            'llm_version': llm_version,
            'llm_temperature': llm_temperature,
            'llm_max_tokens': llm_max_tokens
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

        # Additional LLM-related config
        llm_api_key = None
        embedding_model_version = None
        embedding_dimensions = None

        url = f"{jarvispy_url}/api/v1/rag"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        payload = {
            'question': question,
            'virtual_kg': virtual_kg,
            'to_explain': to_explain,
            'llm_api_key': llm_api_key,
            'embedding_model_version': embedding_model_version,
            'embedding_dimensions': embedding_dimensions
        }

        response = requests.post(url, headers=headers, json=payload)
        return response
    
    @staticmethod
    def chat(question, facts_and_explanations, translated_question_rules, top_retrieved_facts, predicates_and_models, to_explain):
        jarvispy_url = config['JARVISPY_URL']
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")

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
            "llm_api_key": None,
            "llm_version": None,
            "llm_temperature": None,
            "llm_max_tokens": None
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
            "llm_api_key": config.get("LLM_API_KEY"),
            "llm_version": config.get("LLM_VERSION"),
            "llm_temperature": config.get("LLM_TEMPERATURE"),
            "llm_max_tokens": config.get("LLM_MAX_TOKENS")
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
        
        url = f"{jarvispy_url}/api/v1/infer-schema"
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
    def all_pairs_join(databases: list[Database], to_evaluate: bool, parallel: bool):
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
            "toEvaluate": to_evaluate,
            "parallel": parallel
        }

        response = requests.post(url, headers=headers, json=payload)
        return response