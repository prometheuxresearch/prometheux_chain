import yaml
import os

class Config:
    def __init__(self, config_file=None):
        self.config_file = config_file or os.path.join(os.path.dirname(__file__), 'config.yaml')
        self._config = self._load_config_from_file(self.config_file)

    def _load_config_from_file(self, config_file):
        """Load configuration from a YAML file."""
        if not os.path.exists(config_file):
            return {}
        try:
            with open(config_file, 'r') as file:
                return yaml.safe_load(file) or {}
        except (IOError, yaml.YAMLError) as e:
            print(f"Error loading configuration file: {e}")
            return {}

    def _load_config_from_dict(self, config_dict):
        """Load configuration from a dictionary."""
        return config_dict or {}

    def load_config(self, config_file=None, config_dict=None, merge=False):
        """
        Load configuration from a file or a dictionary.

        :param config_file: Path to the external YAML file.
        :param config_dict: Dictionary containing configuration data.
        :param merge: If True, merge the new configuration with the existing one. 
                      If False, replace the current configuration.
        """
        new_config = {}

        if config_file:
            new_config = self._load_config_from_file(config_file)

        if config_dict:
            dict_config = self._load_config_from_dict(config_dict)
            new_config.update(dict_config)

        if merge:
            self._config.update(new_config)
        else:
            self._config = new_config

        self._save_config()

    def get(self, key, default=None):
        """Retrieve a configuration value by key."""
        return self._config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value by key."""
        self._config[key] = value
        self._save_config()

    def update_config(self, updates):
        """
        Update multiple configuration values from a dictionary.
        
        :param updates: A dictionary of keys and values to update.
        """
        self._config.update(updates)
        self._save_config()

    def get_all(self):
        """Get the entire configuration as a dictionary."""
        return self._config.copy()  # Return a copy to prevent external modification

    def _save_config(self):
        """Save the current configuration to the YAML file."""
        try:
            with open(self.config_file, 'w') as file:
                yaml.dump(self._config, file)
        except IOError as e:
            print(f"Error saving configuration file: {e}")

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

# Create a single instance of the Config class that can be imported
config = Config()