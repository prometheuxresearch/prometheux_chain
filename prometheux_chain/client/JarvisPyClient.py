from ..config import config
import requests
import os
import json


class JarvisPyClient:

    @staticmethod
    def set_config_prop(key, value):
        headers = {'Content-Type': 'application/json'}
        params = {'key': key, 'value': value}
        response = requests.get(f"{config['JARVISPY_URL']}/config-info/set", headers=headers, params=params)
        return response

    @staticmethod
    def update_llm_configs():
        """
        Updates the LLM configuration on the backend by setting relevant properties
        such as the OpenAI API key, embedding model, and embedding dimensions.
        """
        if JarvisPyClient.is_reachable():
            # OpenAI API Key
            if config.get("OPENAI_API_KEY"):
                set_prop_response = JarvisPyClient.set_config_prop("OPENAI_API_KEY", config.get("OPENAI_API_KEY"))
                if set_prop_response.status_code != 200:
                    raise Exception(
                        f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")
            else:
                raise Exception("OPENAI_API_KEY is not set in config.")

            # OpenAI Model
            if config.get("OPENAI_MODEL"):
                set_prop_response = JarvisPyClient.set_config_prop("OPENAI_MODEL", config.get("OPENAI_MODEL"))
                if set_prop_response.status_code != 200:
                    raise Exception(
                        f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")
            else:
                raise Exception("OPENAI_MODEL is not set in config.")

            # OpenAI Embedding Model
            if config.get("OPENAI_EMBEDDING_MODEL"):
                set_prop_response = JarvisPyClient.set_config_prop("OPENAI_EMBEDDING_MODEL",
                                                                   config.get("OPENAI_EMBEDDING_MODEL"))
                if set_prop_response.status_code != 200:
                    raise Exception(
                        f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")
            else:
                raise Exception("OPENAI_EMBEDDING_MODEL is not set in config.")

            # OpenAI Embedding Dimensions
            if config.get("OPENAI_EMBEDDING_DIMENSIONS"):
                set_prop_response = JarvisPyClient.set_config_prop("OPENAI_EMBEDDING_DIMENSIONS",
                                                                   config.get("OPENAI_EMBEDDING_DIMENSIONS"))
                if set_prop_response.status_code != 200:
                    raise Exception(
                        f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")
            else:
                raise Exception("OPENAI_EMBEDDING_DIMENSIONS is not set in config.")

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
    def graph_rag(question=None, vadalog_program=None):
        """
        Sends a natural language question to the backend's graph_rag endpoint.

        Parameters:
            question (str): The user's natural language question.
            vadalog_program (str): The content of the .vada file.

        Returns:
            list: A list of strings returned by the backend.

        Raises:
            Exception: If there's an error in the request or response.
        """
        if(not question and not vadalog_program):
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
            'question' : question,
            'vadalog_program': vadalog_program,
            'model': config.get('MODEL', 'gpt-4'),
            'temperature': config.get('TEMPERATURE', 0.5),
            'embedding_model': config.get('EMBEDDING_MODEL', 'text-embedding-3-large'),
            'embedding_dimensions': config.get('EMBEDDING_DIMENSIONS', 2048)
        }

        # Send the POST request with JSON data
        response = requests.post(f"{config['JARVISPY_URL']}/api/graphRAG", headers=headers, json=data)
        response_json = response.json()
        if response.status_code == 200:
            return response_json['data']
        else:
            return (f"Graph RAG failed with error: {response_json['message']}")