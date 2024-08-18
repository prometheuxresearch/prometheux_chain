from .Rule import Rule
from .Ontology import Ontology
from ..client.JarvisClient import JarvisClient

def compile_vadalog(file_paths):

    if isinstance(file_paths, str):
        file_paths = [file_paths]
    
    ontologies:list[Ontology] = []

    i = 1
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                vadalog_program = file.read()
        except IOError as e:
            print(f"Error opening file {file_path}: {e}")
            return None
        rule = Rule(None, vadalog_program, "Description of the rule", 1)
        ontology = Ontology(id=None, name="", short_description="", long_description="", domain_knowledge="")
        ontology.add_rule(rule)
        response = JarvisClient.compile_logic(ontology)
        ordinal = lambda n: "%d%s" % (n, "th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))
        ordinal_i = ordinal(i)
        if response.status_code != 200:
            raise Exception(f"Compilation error at {ordinal_i} program! Detail: {response.json()['message']}")
        else:
            print(f"Compilation succesfully completed for the {ordinal_i} program. Detail: {response.json()['message']}")
        compiled_ontology_response = response.json()["data"]
        compiled_ontology = Ontology.from_dict(compiled_ontology_response)
        compiled_ontology.set_vada_file_path(file_path)
        ontologies.append(compiled_ontology)
        i = i+1
    return ontologies