from ..logic.Ontology import Ontology
from ..logic.Rule import Rule
from ..config import config
import json
import requests

# Ensure the compile_logic method is properly implemented to handle the request
class JarvisClient:
    @staticmethod
    def compile_logic(ontology):
        url = f"{config['JARVIS_URL']}/ontology-info/compileLogic"
        headers = {'Content-Type': 'application/json'}
        
        try:
            # Directly serialize the ontology object to a JSON string
            json_data = ontology.to_dict()
            response = requests.post(url, headers=headers, json=json_data)  # Use 'json' parameter to ensure proper headers
            response.raise_for_status()  # This will handle HTTP errors
        except requests.RequestException as e:
            # Properly log or handle the exception
            raise Exception(f"An error occurred during HTTP request: {e}")
        
        return response.json()

# Ontology's to_dict method
def to_dict(self):
    return {
        'id': self.id,
        'name': self.name,
        'shortDescription': self.short_description,
        'longDescription': self.long_description,
        'domainKnowledge': self.domain_knowledge,
        'rules': [rule.to_dict() for rule in self.rules]  # This serializes each Rule into a dictionary
    }
