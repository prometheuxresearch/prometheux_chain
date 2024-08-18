from ..logic.Ontology import Ontology
from ..logic.Bind import Bind
from typing import List

class KnowledgeGraph:
    def __init__(self, id=None, name="", ontologies:List[Ontology]=None, databases=None, bindings:list[Bind]=None, schema="", for_chase=False, params:dict={}):
        self.id = id
        self.name = name
        self.ontologies = ontologies if ontologies is not None else []
        self.databases = databases if databases is not None else []
        self.bindings = bindings if bindings is not None else []
        self.schema = schema
        self.forChase = for_chase
        self.params = params

    def to_dict(self):
        """Converts the object to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "ontologies": [ontology.to_dict() for ontology in self.ontologies],
            "databases": self.databases,
            "bindings": [binding.to_dict() for binding in self.bindings],
            "schema": self.schema,
            "forChase": self.forChase,
            "params" : self.params
        }

    @classmethod
    def from_dict(cls, data):
        ontologies = [Ontology.from_dict(o) for o in data.get('ontologies', [])]
        bindings = [Bind.from_dict(b) for b in data.get('bindings', [])]
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            ontologies=ontologies,
            databases=data.get('databases', []),
            bindings=bindings,
            schema=data.get('schema', "\{\}"),
            for_chase=data.get('forChase', False),
            params = data.get('params')
        )