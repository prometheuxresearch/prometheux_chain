from ..logic.KnowledgeGraph import KnowledgeGraph
from ..client.JarvisClient import JarvisClient
from ..logic.BindTable import BindTable
from ..logic.Ontology import Ontology
from ..logic.PredicateInfo import PredicateInfo
from ..reasoning.ReasoningResult import ReasoningResult
import uuid

def reason(ontology : Ontology, bind_input_table: BindTable, bind_output_table: BindTable, for_explanation=False):
    input_bindings = bind_input_table.get_bindings()
    databases = []
    for input_bind in input_bindings:
        databases.append(input_bind.get_datasource().get_database_info_id())
    
    first_output_bind = bind_output_table.bindings[0]

    output_predicate = PredicateInfo(first_output_bind.predicate_name)
    ontology.outputPredicates = [output_predicate]
    #name = ""
    name = "default_"+str(uuid.uuid4())
    knowledge_graph = KnowledgeGraph(None, name, [ontology], databases, input_bindings, "[]", for_explanation)
    store_response = JarvisClient.store_knowledge_graph(knowledge_graph)
    # 409 means conflict: a kg having that name already exists
    if store_response.status_code == 409:
        print(store_response.json()["message"])
    elif store_response.status_code != 200:
        raise Exception(f"HTTP error! status: {store_response.status_code}, detail: {store_response.text}")
    if store_response.status_code == 200:
        store_response.text
    stored_knowledge_graph = KnowledgeGraph.from_dict(store_response.json()["data"])
    reasoning_response = JarvisClient.reason(stored_knowledge_graph)
    print(reasoning_response.json()["message"])
    return ReasoningResult(output_predicate.name, stored_knowledge_graph.id)

