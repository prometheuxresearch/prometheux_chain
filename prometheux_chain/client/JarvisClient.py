from ..config import config
import requests
import json
from ..logic.KnowledgeGraph import KnowledgeGraph
from ..logic.Fact import Fact

class JarvisClient:
    @staticmethod
    def compile_logic(ontology):
        url = f"{config['JARVIS_URL']}/ontology-info/compileLogic"
        headers = {'Content-Type': 'application/json'}
        json_data = ontology.to_dict()
        response = requests.post(url, headers=headers, json=json_data)
        return response
    
    @staticmethod
    def store_knowledge_graph(knowledge_graph: KnowledgeGraph):
        url = f"{config['JARVIS_URL']}/knowledgegraph-info/store"
        headers = {'Content-Type': 'application/json'}
        
        data = json.dumps(knowledge_graph.to_dict())

        response = requests.post(url, headers=headers, data=data)
        return response
    
    @staticmethod
    def reason(knowledge_graph: KnowledgeGraph):
        url = f"{config['JARVIS_URL']}/reasoningtask-info/reason"
        headers = {'Content-Type': 'application/json'}
        
        data = json.dumps(knowledge_graph.to_dict())

        response = requests.post(url, headers=headers, data=data)
        return response

    @staticmethod
    def get_potential_bindings(ontology2Databases):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(ontology2Databases.to_dict())

        response = requests.post(f"{config['JARVIS_URL']}/ontology-info/getPotentialBindings", headers=headers, data=data)

        if response.status_code != 200:
            raise Exception(f"HTTP error! status: {response.status_code}, detail: {response.json().message}")

        return response
    
    @staticmethod
    def get_chase_facts(output_predicate, knowledge_graph_id, page,size,sort_property,asc):
        headers = {'Content-Type': 'application/json'}
        params = {}
        params['factPredicate'] = output_predicate
        params['knowledgeGraphId'] = knowledge_graph_id
        params['page'] = page
        params['size'] = size
        params['sortProperty'] = sort_property
        params['asc'] = asc
        response = requests.get(f"{config['JARVIS_URL']}/chasefact-info/paged/startswith", headers=headers, params=params)
        return response
    
    @staticmethod
    def set_config_prop(key, value):
        headers = {'Content-Type': 'application/json'}
        params = {}
        params['key'] = key
        params['value'] = value
        response = requests.get(f"{config['JARVIS_URL']}/config-info/set", headers=headers, params=params)
        return response


    @staticmethod
    def explain_by_fact(structured_fact : Fact, glossary):
        headers = {'Content-Type': 'application/json'}
        params = {}
        params['fact'] = structured_fact.fact
        params['textualExplanation'] = structured_fact.textual_explanation
        params['visualExplanation'] = structured_fact.visual_explanation
        params['chaseExplanation'] = structured_fact.chase_explanation
        params['isForChase'] = structured_fact.is_for_chase
        params['reasoningTaskId'] = structured_fact.reasoning_task_id
        params['knowledgeGraphId'] = structured_fact.knowledge_graph_id
        params['doVisualAndChaseExplanation'] = False
        params['doTextualExplanation'] = True
        if glossary:
            params['glossary'] = glossary
        response = requests.get(f"{config['JARVIS_URL']}/chasefact-info/explainByFact", headers=headers, params=params)
        return response
    
    @staticmethod
    def explain(fact, glossary):
        headers = {'Content-Type': 'application/json'}
        params = {}
        params['factToExplain'] = fact
        params['doVisualAndChaseExplanation'] = False
        params['doTextualExplanation'] = True
        if glossary:
            params['glossary'] = glossary
        response = requests.get(f"{config['JARVIS_URL']}/chasefact-info/explain", headers=headers, params=params)
        return response