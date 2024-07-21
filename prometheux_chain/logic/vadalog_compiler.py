import os
from .Rule import Rule
from .Ontology import Ontology
from ..client.JarvisClient import JarvisClient
import json

def compile_vadalog(file_path):
    with open(file_path, 'r') as file:
        vadalog_content = file.read()

    rule = Rule(None, vadalog_content, "Description of the rule", 1)

    ontology = Ontology(id=None, name="", short_description="", long_description="", domain_knowledge="")

    ontology.add_rule(rule)

    response = JarvisClient.compile_logic(ontology).json()
    ontology = response["data"]
    return Ontology.from_dict(ontology)