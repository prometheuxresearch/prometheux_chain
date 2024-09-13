from .PredicateInfo import PredicateInfo
from .Rule import Rule
import pandas as pd
from IPython.display import display
from typing import List

class Ontology:
    def __init__(self, id, name, short_description, long_description, domain_knowledge):
        self.id = id
        self.name = name
        self.shortDescription = short_description
        self.longDescription = long_description
        self.domainKnowledge = domain_knowledge
        self.inputPredicates:List[PredicateInfo] = []
        self.intensionalPredicates:List[PredicateInfo] = []
        self.outputPredicates:List[PredicateInfo] = []
        self.rules:List[Rule] = []
        self.vada_file_path = ""

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_input_predicate(self, predicate):
        self.inputPredicates.append(predicate)

    def add_intensional_predicate(self, predicate):
        self.intensionalPredicates.append(predicate)

    def add_output_predicate(self, predicate):
        self.outputPredicates.append(predicate)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'shortDescription': self.shortDescription,
            'longDescription': self.longDescription,
            'domainKnowledge': self.domainKnowledge,
            'inputPredicates': [predicate.to_dict() for predicate in self.inputPredicates],
            'intensionalPredicates': [predicate.to_dict() for predicate in self.intensionalPredicates],
            'outputPredicates': [predicate.to_dict() for predicate in self.outputPredicates],
            'rules': [rule.to_dict() for rule in self.rules]
        }

    def merge(self, ontology: 'Ontology'):
        #self.inputPredicates:List[PredicateInfo] = []
        #self.intensionalPredicates:List[PredicateInfo] = []
        #self.outputPredicates:List[PredicateInfo] = []
        #self.rules:List[Rule] = []
        for predicateInfo in ontology.inputPredicates:
            self.add_input_predicate(predicateInfo)
        for predicateInfo in ontology.intensionalPredicates:
            self.add_intensional_predicate(predicateInfo)
        for predicateInfo in ontology.outputPredicates:
            self.add_output_predicate(predicateInfo)
        for rule in ontology.rules:
            self.add_rule(rule)
        self.longDescription += "\n\n"+ontology.longDescription
        self.shortDescription += "\n\n"+ontology.shortDescription
        self.domainKnowledge += "\n\n"+ontology.domainKnowledge
        
        


    @classmethod
    def from_dict(cls, data):
        ontology = cls(
            id=data['id'],
            name=data['name'],
            short_description=data['shortDescription'],
            long_description=data['longDescription'],
            domain_knowledge=data['domainKnowledge']
        )

        for predicate_data in data['inputPredicates']:
            ontology.add_input_predicate(PredicateInfo.from_dict(predicate_data))
        for predicate_data in data['intensionalPredicates']:
            ontology.add_intensional_predicate(PredicateInfo.from_dict(predicate_data))
        for predicate_data in data['outputPredicates']:
            ontology.add_output_predicate(PredicateInfo.from_dict(predicate_data))
        for rule_data in data['rules']:
            rule = Rule(
                id=rule_data['id'],
                logic=rule_data['logic'],
                nl_description=rule_data['nlDescription'],
                position_in_ontology=rule_data['positionInOntology'],
                file_path=rule_data['filePath']
            )
            ontology.add_rule(rule)
        return ontology

    def show_rules(self, max_rows=None, max_colwidth=None):
        # Create a DataFrame from the rules
        data = [{
            'Logic': rule.logic,
            'Description': rule.nlDescription,
        } for rule in sorted(self.rules, key=lambda x: x.positionInOntology)]
        
        df = pd.DataFrame(data)

        pd.set_option('display.max_rows', max_rows)
        pd.set_option('display.max_columns', max_colwidth)
        pd.set_option('display.expand_frame_repr', False)
        pd.set_option('display.max_colwidth', None)
        display(df)

    def show_summary(self):
        print("\n" + self.longDescription + "\n")
    
    def set_vada_file_path(self, vada_file_path):
        self.vada_file_path = vada_file_path


