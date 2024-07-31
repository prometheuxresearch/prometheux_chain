class Rule:
    def __init__(self, id=None, logic="", nl_description="", position_in_ontology=0):
        self.id = id
        self.logic = logic
        self.nlDescription = nl_description
        self.positionInOntology = position_in_ontology

    def to_dict(self):
        return {
            'id': self.id,
            'logic': self.logic,
            'nlDescription': self.nlDescription,
        }
