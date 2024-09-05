from ..logic.KnowledgeGraph import KnowledgeGraph
from ..client.JarvisClient import JarvisClient
from ..logic.BindTable import BindTable
from ..logic.Ontology import Ontology
from ..logic.PredicateInfo import PredicateInfo
from ..reasoning.ReasoningResult import ReasoningResult
import uuid
from ..chat.vector_index_initializer import VectorIndexInitializer

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