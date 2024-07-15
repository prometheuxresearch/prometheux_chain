import os
from .Rule import Rule
from .Ontology import Ontology
from ..client.JarvisClient import JarvisClient

def compile_vadalog(file_path):
    # Read the entire content of the vadalog file as a single string
    with open(file_path, 'r') as file:
        vadalog_content = file.read()

    # Create a Rule object with the content of the .vada file
    rule = Rule(None, vadalog_content, "Description of the rule", 1)

    # Create an Ontology object
    ontology = Ontology(id=None, name="default", short_description="default", long_description="default", domain_knowledge="default")

    # Add the Rule to the Ontology
    ontology.add_rule(rule)

    # Now serialize and send to Jarvis backend
    response = JarvisClient.compile_logic(ontology)
    
    return response
