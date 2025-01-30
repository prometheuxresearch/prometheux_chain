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
        """
        Checks if the JarvisPy backend URL is reachable by sending a GET request.

        Returns:
            bool: True if the backend is reachable (status code 200-399), False otherwise.
        """
        try:
            response = requests.get(config['JARVISPY_URL'] + "/api/hello", timeout=5)
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

        url = f"{JARVISPY_URL}/api/cleanup"
        headers = {
            'Authorization': f"Bearer {PMTX_TOKEN}",
            'Content-Type': 'application/json'
        }

        # If virtual_kg is given, include it as JSON in the DELETE request
        if virtual_kg:
            response = requests.post(url, headers=headers, json=virtual_kg)
        else:
            response = requests.post(url, headers=headers)

        return response

    @staticmethod
    def reason(programs, params, to_explain, to_persist):
        JARVISPY_URL = config['JARVISPY_URL']
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN'))

        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        url = f"{JARVISPY_URL}/api/reason"
        data = {
            'programs': programs,
            'params': params,
            'to_explain': to_explain,
            'to_persist': to_persist
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

        url = f"{JARVISPY_URL}/api/query"
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

        url = f"{JARVISPY_URL}/api/explain"
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

        url = f"{JARVISPY_URL}/api/visualize"
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
    def rag(question=None, vadalog_program=None):
        """
        Sends a natural language question to the backend's rag endpoint.

        Parameters:
            question (str): The user's natural language question.
            vadalog_program (str): The content of the .vada file.

        Returns:
            list: A list of strings returned by the backend.

        Raises:
            Exception: If there's an error in the request or response.
        """
        if not question and not vadalog_program:
            raise Exception("Please provide a question to ask or a vadalog_program for reasoning or both")

        # Get tokens from environment variables or config
        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', config.get('OPENAI_API_KEY', ''))
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not OPENAI_API_KEY:
            raise Exception("OPENAI_API_KEY is not set. Please set it in the environment variables or config.")
        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in the environment variables or config.")

        # Prepare headers and data for the request
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {PMTX_TOKEN};{OPENAI_API_KEY}"
        }
        data = {
            'question': question,
            'vadalog_program': vadalog_program,
            'model': config.get('MODEL', 'gpt-4'),
            'temperature': config.get('TEMPERATURE', 0.5),
            'embedding_model': config.get('EMBEDDING_MODEL', 'text-embedding-3-large'),
            'embedding_dimensions': config.get('EMBEDDING_DIMENSIONS', 2048)
        }

        # Send the POST request with JSON data
        response = requests.post(f"{config['JARVISPY_URL']}/api/rag", headers=headers, json=data)
        response_json = response.json()
        if response.status_code == 200:
            return response_json['data']
        else:
            return f"Graph RAG failed with error: {response_json['message']}"

    @staticmethod
    def validate(text, guardrail_program):
        JARVISPY_URL = config['JARVISPY_URL']
        PMTX_TOKEN = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))

        if not PMTX_TOKEN:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")

        # Additional LLM-related config
        llm_api_key = config.get('LLM_API_KEY', None)
        llm_provider = config.get('LLM_PROVIDER', None)
        llm_version = config.get('LLM_VERSION', 'gpt-4o')
        llm_temperature = config.get('LLM_TEMPERATURE', 0.50)
        llm_max_tokens = config.get('LLM_MAX_TOKENS', 2000)

        url = f"{JARVISPY_URL}/api/validate"
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
