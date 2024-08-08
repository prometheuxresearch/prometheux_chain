import yaml
import os
from client.JarvisClient import JarvisClient

class Config:
    def __init__(self, config_file=None):
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), 'config.yaml')
        self.config_file = config_file
        self._config = self._load_config()

    def _load_config(self):
        with open(self.config_file, 'r') as file:
            return yaml.safe_load(file)

    def get(self, key):
        return self._config.get(key)
    
    def set(self, key, value):
        if key in ["LLM", "OPENAI_API_KEY"]:
            set_prop_response = JarvisClient.set_config_prop(key, value)
            if set_prop_response.status_code != 200:
                raise Exception(f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")
        self._config[key] = value
        self._save_config()

    def _save_config(self):
        with open(self.config_file, 'w') as file:
            yaml.dump(self._config, file)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

# Create a single instance of the Config class that can be imported
config = Config()
