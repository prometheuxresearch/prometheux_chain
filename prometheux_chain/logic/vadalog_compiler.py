from .Rule import Rule
from .Ontology import Ontology
from ..client.JarvisClient import JarvisClient
import re
import time


def compile_vadalog(file_paths, attempts=0):
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    ontologies: list[Ontology] = []

    i = 1
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                vadalog_program = file.read()
        except IOError as e:
            raise Exception(f"Error opening file {file_path}: {e}")

        rule = Rule(None, vadalog_program, "Description of the rule", 1)
        ontology = Ontology(id=None, name="", short_description="", long_description="", domain_knowledge="")
        ontology.add_rule(rule)
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
        compiled_ontology.set_vada_file_path(file_path)
        ontologies.append(compiled_ontology)

        # Now update the .vada file with the module annotations featuring the nl description, if generated
        update_vada_file_with_summary(file_path, compiled_ontology)

        i += 1

    return ontologies


def update_vada_file_with_summary(vada_file_path, compiled_ontology):
    with open(vada_file_path, 'r') as file:
        vada_lines = file.readlines()

    # Loop over the ontology rules (which contain the updated @model annotations)
    for rule in compiled_ontology.rules:
        # Extract the first argument from the rule.logic (the argument that defines the model)
        model_id_match = re.match(r'@model\("([^"]+)",', rule.logic.strip())
        if model_id_match:
            model_id = model_id_match.group(1)  # This is the first argument (the model identifier)

            # The updated @model annotation is the full logic of the rule
            updated_model_annotation = rule.logic.strip()

            # Prepare a regular expression to find the corresponding model annotation in the vada file
            model_regex = re.compile(rf'@model\("{model_id}",')

            # Search for the corresponding @model annotation in the vada file
            start_index = -1
            for i, line in enumerate(vada_lines):
                # If the line matches the start of the @model annotation, mark the starting point
                if model_regex.search(line):
                    start_index = i
                    break
            if start_index != -1:
                # Now gather the lines that form the complete multi-line @model annotation
                end_index = start_index
                while not vada_lines[end_index].strip().endswith(').'):
                    end_index += 1

                # Check if the annotation is already the same, skip if no change
                current_annotation = ''.join(vada_lines[start_index:end_index + 1]).strip()
                if current_annotation != updated_model_annotation:
                    # Replace the multi-line @model annotation with the updated version from the ontology
                    vada_lines[start_index:end_index + 1] = [updated_model_annotation + '\n']

    # Overwrite the original .vada file with the updated content
    with open(vada_file_path, 'w') as updated_file:
        updated_file.writelines(vada_lines)

