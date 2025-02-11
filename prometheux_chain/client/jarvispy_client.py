from ..config import config
import requests
import os

"""
JarvisPy Client Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


class JarvisPyClient:

    @staticmethod
    def is_reachable():
        try:
            response = requests.get(config['JARVISPY_URL'] + "/api/v1/hello", timeout=5)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            return False

    @staticmethod
    def delete_virtual_kg_resources(virtual_kg=None):
        JARVISPY_URL = config['JARVISPY_URL']
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in env variables or config.")

        url = f"{JARVISPY_URL}/api/v1/cleanup"
        headers = {
            'Authorization': f"Bearer {PMTX_TOKEN}",
            'Content-Type': 'application/json'
        }

        if virtual_kg:
            response = requests.post(url, headers=headers, json=virtual_kg)
        else:
            response = requests.post(url, headers=headers)
        return response

    @staticmethod
    def compile(ontology):
        # Example config usage
        JARVISPY_URL = config['JARVISPY_URL']
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN'))

        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        url = f"{JARVISPY_URL}/api/v1/compile"
        data = {'ontology': ontology}
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {PMTX_TOKEN}"
        }

        response = requests.post(url, json=data, headers=headers)

        # 1) Check status code
        if response.status_code != 200:
            # Attempt to parse any JSON error message
            try:
                response_json = response.json()
                error_msg = response_json.get("message", "Unknown error from backend.")
            except Exception:
                # Fallback to response text
                error_msg = response.text or "Unknown error from backend."
            raise RuntimeError(f"Compilation failed (HTTP {response.status_code}). {error_msg}")

        # 2) If 200, parse the JSON
        try:
            response_json = response.json()
        except Exception as e:
            raise RuntimeError(f"Failed to parse JSON response from JarvisPy backend: {str(e)}")

        # 3) Check if the backend explicitly indicates error in JSON
        if response_json.get("status") == "error":
            error_msg = response_json.get("message", "Unknown error from backend.")
            raise RuntimeError(f"Compilation failed: {error_msg}")

        # 4) Otherwise, assume success:
        return response_json

    @staticmethod
    def reason(vadalog_programs, vadalog_params, to_explain, to_persist, to_embed):
        JARVISPY_URL = config['JARVISPY_URL']
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN'))

        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")
        
        # Additional LLM-related config
        llm_api_key = config.get('LLM_API_KEY', None)
        llm_provider = config.get('LLM_PROVIDER', 'OpenAI')
        embedding_model_version = config.get('EMBEDDING_MODEL_VERSION', 'text-embedding-3-large')
        embedding_dimensions = config.get('EMBEDDING_DIMENSIONS', 2048)

        url = f"{JARVISPY_URL}/api/v1/reason"
        data = {
            'vadalog_programs': vadalog_programs,
            'vadalog_params': vadalog_params,
            'to_explain': to_explain,
            'to_persist': to_persist,
            'to_embed': to_embed,
            'llm_api_key': llm_api_key,
            'llm_provider': llm_provider,
            'embedding_model_version': embedding_model_version,
            'embedding_dimensions': embedding_dimensions
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {PMTX_TOKEN}"
        }

        response = requests.post(url, json=data, headers=headers)
        return response

    @staticmethod
    def query(virtual_kg, query, params, language_type):
        JARVISPY_URL = config['JARVISPY_URL']
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        url = f"{JARVISPY_URL}/api/v1/query"
        data = {
            'virtual_kg': virtual_kg,
            'query': query,
            'params': params,
            'language_type': language_type
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {PMTX_TOKEN}"
        }

        response = requests.post(url, json=data, headers=headers)
        return response

    @staticmethod
    def explain(virtual_kg, fact_to_explain):
        JARVISPY_URL = config['JARVISPY_URL']
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        url = f"{JARVISPY_URL}/api/v1/explain"
        data = {
            'fact_to_explain': fact_to_explain,
            'virtual_kg': virtual_kg
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {PMTX_TOKEN}"
        }

        response = requests.post(url, json=data, headers=headers)
        return response

    @staticmethod
    def visualize(vadalog_program: str):
        JARVISPY_URL = config['JARVISPY_URL']
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))
        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        url = f"{JARVISPY_URL}/api/v1/visualize"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {PMTX_TOKEN}"
        }
        data = {
            'vadalog_program': vadalog_program
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    @staticmethod
    def validate(text, guardrail_program):
        JARVISPY_URL = config['JARVISPY_URL']
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")

        # Additional LLM-related config
        llm_api_key = config.get('LLM_API_KEY', None)
        llm_provider = config.get('LLM_PROVIDER', 'OpenAI')
        llm_version = config.get('LLM_VERSION', 'gpt-4o')
        llm_temperature = config.get('LLM_TEMPERATURE', 0.50)
        llm_max_tokens = config.get('LLM_MAX_TOKENS', 2000)

        url = f"{JARVISPY_URL}/api/v1/validate"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {PMTX_TOKEN}"
        }
        data = {
            'text': text,
            'guardrail_program': guardrail_program,
            'llm_api_key': llm_api_key,
            'llm_provider': llm_provider,
            'llm_version': llm_version,
            'llm_temperature': llm_temperature,
            'llm_max_tokens': llm_max_tokens
        }

        response = requests.post(url, headers=headers, json=data)
        return response

    @staticmethod
    def rag(question, virtual_kg, to_explain):
        if not question and not virtual_kg:
            raise Exception("Please provide a question to ask and a virtual knowledge graph")

        JARVISPY_URL = config['JARVISPY_URL']
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")

        # Additional LLM-related config
        llm_api_key = config.get('LLM_API_KEY', None)
        llm_provider = config.get('LLM_PROVIDER', 'OpenAI')
        embedding_model_version = config.get('EMBEDDING_MODEL_VERSION', 'text-embedding-3-large')
        embedding_dimensions = config.get('EMBEDDING_DIMENSIONS', 2048)

        url = f"{JARVISPY_URL}/api/v1/rag"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {PMTX_TOKEN}"
        }
        data = {
            'question': question,
            'virtual_kg': virtual_kg,
            'to_explain': to_explain,
            'llm_api_key': llm_api_key,
            'llm_provider': llm_provider,
            'embedding_model_version': embedding_model_version,
            'embedding_dimensions': embedding_dimensions
        }

        response = requests.post(url, headers=headers, json=data)
        return response
    
    @staticmethod
    def chat(question, facts_and_explanations):
        JARVISPY_URL = config['JARVISPY_URL']
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")

        url = f"{JARVISPY_URL}/api/v1/chat"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {PMTX_TOKEN}"
        }
        data = {
            "question": question,
            "facts_and_explanations": facts_and_explanations,
            "llm_api_key": config.get("LLM_API_KEY"),
            "llm_version": config.get("LLM_VERSION"),
            "llm_temperature": config.get("LLM_TEMPERATURE"),
            "llm_max_tokens": config.get("LLM_MAX_TOKENS")
        }
        response = requests.post(url, headers=headers, json=data)
        return response
    
    @staticmethod
    def translate(domain_knowledge):
        JARVISPY_URL = config['JARVISPY_URL']
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        
        url = f"{JARVISPY_URL}/api/v1/translate_nl_to_vadalog"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {PMTX_TOKEN}"
        }
        data = {
            "domain_knowledge": domain_knowledge,
            "llm_api_key": config.get("LLM_API_KEY"),
            "llm_version": config.get("LLM_VERSION"),
            "llm_temperature": config.get("LLM_TEMPERATURE"),
            "llm_max_tokens": config.get("LLM_MAX_TOKENS")
        }
        response = requests.post(url, headers=headers, json=data)
        return response
        