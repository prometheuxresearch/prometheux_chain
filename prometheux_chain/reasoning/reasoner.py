from ..logic.KnowledgeGraph import KnowledgeGraph
from ..client.JarvisClient import JarvisClient
from ..client.VadalogClient import VadalogClient
from ..logic.BindTable import BindTable
from ..logic.Ontology import Ontology
from ..logic.PredicateInfo import PredicateInfo
from ..reasoning.ReasoningResult import ReasoningResult
from ..reasoning.Fact import Fact
import uuid

def reason(ontologies, bind_input_table: BindTable = None, bind_output_table: BindTable = None, for_explanation=False, params : dict = {}):
    if isinstance(ontologies, Ontology):
        ontologies = [ontologies]
    elif isinstance(ontologies, list):
        if not all(isinstance(o, Ontology) for o in ontologies):
            raise ValueError("All elements in the ontologies list must be Ontology instances.")
        if bind_input_table is not None or bind_output_table is not None:
            raise AssertionError("bind_input_table and bind_output_table must both be None when ontologies is a list.")
    else:
        raise TypeError("ontologies must be either an Ontology instance or a list of Ontology instances.")
    
    i = 1
    reasoning_results: list[ReasoningResult] = []
    for ontology in ontologies:
        ordinal = lambda n: "%d%s" % (n, "th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))
        ordinal_i = ordinal(i)
        print(f"Started reasoning for the {ordinal_i} program")
        reasoning_result: ReasoningResult = reason_on_single_ontology(ontology, bind_input_table, bind_output_table, for_explanation, params)
        if reasoning_result.reasoning_status_code != 200:
            raise Exception(f"Reasoning error at {ordinal_i} program! Status: {reasoning_result.reasoning_status_code}. Detail: {reasoning_result.reasoning_message}")
        else:
            print(f"Reasoning completed for the {ordinal_i} program. Status: {reasoning_result.reasoning_status_code}. Detail: {reasoning_result.reasoning_message}")
        reasoning_results.append(reasoning_result)
        i += 1
    return reasoning_results


def reason_on_single_ontology(ontology: Ontology, bind_input_table: BindTable, bind_output_table: BindTable, for_explanation, params):
    databases = []
    input_bindings = []
    output_bindings = []
    if bind_input_table:
        input_bindings = bind_input_table.get_bindings()
        for input_bind in input_bindings:
            databases.append(input_bind.get_datasource().get_database_info_id())
    
    if bind_output_table:
        output_bindings = bind_output_table.bindings
        for output_binding in output_bindings:
            output_predicate = PredicateInfo(output_binding.predicate_name)
            ontology.outputPredicates.append(output_predicate)
    #name = ""
    name = "default_"+str(uuid.uuid4())
    knowledge_graph = KnowledgeGraph(None, name, [ontology], databases, input_bindings, "[]", for_explanation, params)
    store_response = JarvisClient.store_knowledge_graph(knowledge_graph)
    # 409 means conflict: a kg having that name already exists
    if store_response.status_code != 200:
        return ReasoningResult(-1, store_response.status_code, store_response.json()["message"])
    stored_knowledge_graph = KnowledgeGraph.from_dict(store_response.json()["data"])
    reasoning_response = JarvisClient.reason(stored_knowledge_graph)
    return ReasoningResult(stored_knowledge_graph.id, reasoning_response.status_code, reasoning_response.json()["message"])



def perform(vada_file_paths, params={}):
    for k in params:
        if isinstance(params[k], str):
            params[k] = f'"{params[k]}"'
    
    ontologiesPaths = []
    if isinstance(vada_file_paths, str):
        ontologiesPaths = [[vada_file_paths]]
    elif isinstance(vada_file_paths, list):
        # it can be a list of ontologies
        for ontologyPaths in vada_file_paths:
            if isinstance(ontologyPaths, str):
                ontologiesPaths.append([ontologyPaths])
            elif isinstance(ontologyPaths, list):
                ontologiesPaths.append(ontologyPaths)

    i = 1
    output_facts: list[Fact] = []
    for ontologiesPath in ontologiesPaths:
        for ontologyPath in ontologiesPath:
            try:
                with open(ontologyPath, 'r') as file:
                    vadalog_program = file.read()
            except IOError as e:
                raise Exception(f"Error opening file {ontologyPath}: {e}")
        
        response = VadalogClient.evaluateWithParams(vadalog_program, params)
        ordinal = lambda n: "%d%s" % (n, "th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))
        ordinal_i = ordinal(i)

        if response.status_code != 200 and response.status_code != 504:
            raise Exception(f"Evaluation error at {ordinal_i} program! Detail: {response.json()['message']}")
        else:
            print(
                f"Evaluation successfully completed for the {ordinal_i} program.")
        
        evaluation_response = response.json()["data"]

        # Iterate over the resultSet and create Fact instances
        for predicate_name, arguments_list in evaluation_response.get('resultSet', {}).items():
            types = evaluation_response.get('types', {}).get(predicate_name, [])
            column_names = evaluation_response.get('columnNames', {}).get(predicate_name, [])
            for arguments in arguments_list:
                fact = Fact(predicate_name, arguments, column_names, types)
                output_facts.append(fact)
        i += 1

    return output_facts