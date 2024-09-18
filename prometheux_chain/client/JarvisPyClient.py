from ..config import config
import requests

class JarvisPyClient:

    @staticmethod
    def set_config_prop(key, value):
        headers = {'Content-Type': 'application/json'}
        params = {}
        params['key'] = key
        params['value'] = value
        response = requests.get(f"{config['JARVISPY_URL']}/config-info/set", headers=headers, params=params)
        return response

    @staticmethod
    def update_llm_configs():
        if JarvisPyClient.is_reachable():
            if config.get("OPENAI_API_KEY"):
                set_prop_response = JarvisPyClient.set_config_prop("OPENAI_API_KEY", config.get("OPENAI_API_KEY"))
                if set_prop_response.status_code != 200:
                    raise Exception(
                        f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")
            if config.get("OPENAI_MODEL"):
                set_prop_response = JarvisPyClient.set_config_prop("OPENAI_MODEL", config.get("OPENAI_MODEL"))
                if set_prop_response.status_code != 200:
                    raise Exception(
                        f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")
            if config.get("OPENAI_TEMPERATURE"):
                set_prop_response = JarvisPyClient.set_config_prop("OPENAI_TEMPERATURE", config.get("OPENAI_TEMPERATURE"))
                if set_prop_response.status_code != 200:
                    raise Exception(
                        f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")

    @staticmethod    
    def is_reachable():
        """
        Checks if a URL is reachable by sending a GET request.

        Parameters:
            url (str): The URL to check.

        Returns:
            bool: True if the URL is reachable (status code 200-399), False otherwise.
        """
        try:
            response = requests.get(config['JARVISPY_URL']+"/api/hello", timeout=5)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            return False