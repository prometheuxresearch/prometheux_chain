from ..logic.Ontology import Ontology

class Ontology2Databases:
    def __init__(self, ontology: Ontology, databases_ids, input=True):
        self.ontology = ontology
        self.databases_ids = databases_ids
        self.input = input

    def to_dict(self):
        return {
            'ontology': self.ontology.to_dict(),
            'databasesIds': self.databases_ids,
            'input' : self.input
        }


