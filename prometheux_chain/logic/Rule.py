class Rule:
    def __init__(self, id=None, logic="", nl_description="", position_in_ontology=0, file_path=""):
        self.id = id
        self.logic = logic
        self.nlDescription = nl_description
        self.positionInOntology = position_in_ontology
        self.file_path = file_path

    def to_dict(self):
        return {
            'id': self.id,
            'logic': self.logic,
            'nlDescription': self.nlDescription,
            'positionInOntology': self.positionInOntology,
            'filePath': self.file_path
        }
