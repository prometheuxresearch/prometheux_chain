from .Rule import Rule
from .Ontology import Ontology
from ..client.JarvisClient import JarvisClient
import re
import time
from collections import defaultdict


def compile_vadalog(file_paths, attempts=0):
    ontologiesPaths = []
    if isinstance(file_paths, str):
        ontologiesPaths = [[file_paths]]
    elif isinstance(file_paths, list):
        # it can be a list of ontologies
        for ontologyPaths in file_paths:
            if isinstance(ontologyPaths, str):
                ontologiesPath = [ontologyPaths]
                ontologiesPaths.append(ontologiesPath)
            elif isinstance(ontologyPaths, list):
                ontologiesPaths.append(ontologyPaths)

    ontologies: list[Ontology] = []

    i = 1
    for ontologiesPath in ontologiesPaths:
        ontology = Ontology(id=None, name="", short_description="", long_description="", domain_knowledge="")
        for ontologyPath in ontologiesPath:
            try:
                with open(ontologyPath, 'r') as file:
                    vadalog_program = file.read()
                    # Pre-process vadalog program, concatenating in single line multi-line model annotations
                    vadalog_program = preprocess_model_annotations(vadalog_program)
                    rule = Rule(None, vadalog_program, "Description of the rule", 1, ontologyPath)
                    ontology.add_rule(rule)
            except IOError as e:
                raise Exception(f"Error opening file {ontologyPath}: {e}")
    
        response = JarvisClient.compile_logic(ontology)
        ordinal = lambda n: "%d%s" % (n, "th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))
        ordinal_i = ordinal(i)

        if response.status_code == 429:
            if attempts == 3:
                raise Exception(
                    f"HTTP error! status: {response.status_code}, detail: {response.json()['message']}")
            print(f"Attempt {attempts}. {response.json()['message']}. Retrying after 5 seconds")
            time.sleep(5)
            attempts += 1
            compile_vadalog(file_paths, attempts)
        if response.status_code != 200:
            raise Exception(f"Compilation error at {ordinal_i} program! Detail: {response.json()['message']}")
        else:
            print(
                f"Compilation successfully completed for the {ordinal_i} program. Detail: {response.json()['message']}")

        compiled_ontology_response = response.json()["data"]
        compiled_ontology = Ontology.from_dict(compiled_ontology_response)
        ontologies.append(compiled_ontology)

        # Now update the .vada file with the module annotations featuring the nl description, if generated
        update_vada_file_with_model_descriptions(compiled_ontology)

        i += 1

    return ontologies


def preprocess_model_annotations(vadalog_program):
    # Regex to find multi-line @model annotations and collapse them into a single line
    model_regex = re.compile(r'@model\s*\((.*?)\)\.', re.DOTALL)
    
    # Replace multi-line @model annotations by collapsing them into a single line
    def collapse_to_single_line(match):
        # Capture everything inside @model(...) and remove newlines
        annotation_content = match.group(1)
        # Replace newlines and excessive whitespace within the captured content
        single_line_annotation = re.sub(r'\s+', ' ', annotation_content).strip()
        return f"@model({single_line_annotation})."
    
    # Apply the regex to collapse all multi-line @model annotations
    vadalog_program = model_regex.sub(collapse_to_single_line, vadalog_program)
    
    return vadalog_program


def update_vada_file_with_model_descriptions(compiled_ontology: Ontology):
    # Step 1: Group rules by their file_path
    rules_by_file = defaultdict(list)
    for rule in compiled_ontology.rules:
        rule_logic_strip = rule.logic.strip()
        rules_by_file[rule.file_path].append(rule_logic_strip)

    print(str(rules_by_file))
    # Step 2: Iterate over each file and apply substitutions
    for vada_file_path, rules in rules_by_file.items():
        # Read the file content
        with open(vada_file_path, 'r') as file:
            vadalog_program = file.read()

        # Step 3: Apply all relevant rule substitutions to the file content
        for rule_logic in rules:
            model_id_match = re.match(r'@model\("([^"]+)",', rule_logic)
            if model_id_match:
                model_id = model_id_match.group(1)  # This is the first argument (the model identifier)

                # Prepare a regular expression to find the corresponding model annotation in the file
                model_regex = re.compile(rf'@model\s*\(\s*"{model_id}",.*?\)\.', re.DOTALL)
                
                # Debug print to check if the pattern is found
                if model_regex.search(vadalog_program):          
                    # Replace the existing @model annotation with the updated rule
                    vadalog_program = model_regex.sub(rule_logic, vadalog_program)
        
        # Step 4: Overwrite the original .vada file with the updated content
        with open(vada_file_path, 'w') as updated_file:
            updated_file.write(vadalog_program)

