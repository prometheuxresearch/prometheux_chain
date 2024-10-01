from ..config import config
import requests
import json
from ..logic.KnowledgeGraph import KnowledgeGraph
from ..logic.Fact import Fact
from .JarvisPyClient import JarvisPyClient


class JarvisClient:
    @staticmethod
    def compile_logic(ontology, user_prompt):
        JarvisClient.update_llm_configs()
        url = f"{config['JARVIS_URL']}/ontology-info/compileLogic"
        headers = {'Content-Type': 'application/json'}
        data = {
            'ontology': ontology.to_dict(),
            'userPrompt': user_prompt
        }        
        response = requests.post(url, headers=headers, json=data)
        return response

    @staticmethod
    def store_knowledge_graph(knowledge_graph: KnowledgeGraph):
        JarvisClient.update_llm_configs()
        url = f"{config['JARVIS_URL']}/knowledgegraph-info/store"
        headers = {'Content-Type': 'application/json'}

        data = json.dumps(knowledge_graph.to_dict())

        response = requests.post(url, headers=headers, data=data)
        return response

    @staticmethod
    def reason(knowledge_graph: KnowledgeGraph):
        JarvisClient.update_llm_configs()
        JarvisPyClient.update_llm_configs()
        url = f"{config['JARVIS_URL']}/reasoningtask-info/reason"
        headers = {'Content-Type': 'application/json'}

        data = json.dumps(knowledge_graph.to_dict())

        response = requests.post(url, headers=headers, data=data)
        return response

    @staticmethod
    def get_potential_bindings(ontology2Databases):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(ontology2Databases.to_dict())

        response = requests.post(f"{config['JARVIS_URL']}/ontology-info/getPotentialBindings", headers=headers,
                                 data=data)

        if response.status_code != 200:
            raise Exception(f"HTTP error! status: {response.status_code}, detail: {response.json().message}")
        
        return response

    @staticmethod
    def get_chase_facts(output_predicate, knowledge_graph_id, page, size, sort_property, asc):
        headers = {'Content-Type': 'application/json'}
        params = {}
        params['factPredicate'] = output_predicate
        params['knowledgeGraphId'] = knowledge_graph_id
        params['page'] = page
        params['size'] = size
        params['sortProperty'] = sort_property
        params['asc'] = asc
        response = requests.get(f"{config['JARVIS_URL']}/chasefact-info/paged/startswith", headers=headers,
                                params=params)
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
    def explain(fact, nl_explanation, user_prompt):
        JarvisClient.update_llm_configs()
        headers = {'Content-Type': 'application/json'}
        params = {
            'factToExplain': fact,
            'doVisualExplanation': False,
            'doChaseExplanation': True,
            'doTextualExplanation': True,
            'doNLTextualExplanation': nl_explanation,
            'userPrompt': user_prompt
        }
        response = requests.get(f"{config['JARVIS_URL']}/chasefact-info/explain", headers=headers, params=params)
        return response

    @staticmethod
    def explain_by_fact(structured_fact: Fact, nl_explanation, user_prompt):
        JarvisClient.update_llm_configs()
        headers = {'Content-Type': 'application/json'}
        params = {
            'fact': structured_fact.fact,
            'textualExplanation': structured_fact.textual_explanation,
            'visualExplanation': structured_fact.visual_explanation,
            'chaseExplanation': structured_fact.chase_explanation,
            'isForChase': structured_fact.is_for_chase,
            'reasoningTaskId': structured_fact.reasoning_task_id,
            'knowledgeGraphId': structured_fact.knowledge_graph_id,
            'doVisualExplanation': False,
            'doChaseExplanation': True,
            'doTextualExplanation': True,
            'doNLTextualExplanation': nl_explanation,
            'userPrompt': user_prompt
        }
        response = requests.get(f"{config['JARVIS_URL']}/chasefact-info/explainByFact", headers=headers, params=params)
        return response

    @staticmethod
    def update_llm_configs():
        if config.get("LLM"):
            set_prop_response = JarvisClient.set_config_prop("LLM", config.get("LLM"))
            if set_prop_response.status_code != 200:
                raise Exception(
                    f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")
        if config.get("OPENAI_API_KEY"):
            set_prop_response = JarvisClient.set_config_prop("OPENAI_API_KEY", config.get("OPENAI_API_KEY"))
            if set_prop_response.status_code != 200:
                raise Exception(
                    f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")
        if config.get("OPENAI_MODEL"):
            set_prop_response = JarvisClient.set_config_prop("OPENAI_MODEL", config.get("OPENAI_MODEL"))
            if set_prop_response.status_code != 200:
                raise Exception(
                    f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")
        if config.get("OPENAI_MAX_TOKENS"):
            set_prop_response = JarvisClient.set_config_prop("OPENAI_MAX_TOKENS", config.get("OPENAI_MAX_TOKENS"))
            if set_prop_response.status_code != 200:
                raise Exception(
                    f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")
        if config.get("OPENAI_TEMPERATURE"):
            set_prop_response = JarvisClient.set_config_prop("OPENAI_TEMPERATURE", config.get("OPENAI_TEMPERATURE"))
            if set_prop_response.status_code != 200:
                raise Exception(
                    f"HTTP error! status: {set_prop_response.status_code}, detail: {set_prop_response.text}")

    @staticmethod
    def queryExplain(nlQuery):
        headers = {'Content-Type': 'application/json'}
        params = {}
        params['nlQuery'] = nlQuery
        response = requests.get(f"{config['JARVIS_URL']}/rag-info/queryExplain", headers=headers, params=params)
        return response

    @staticmethod
    def delete_all_resoning_resources():
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(f"{config['JARVIS_URL']}/deleteAll", headers=headers)
        return response
