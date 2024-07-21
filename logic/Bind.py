from ..model.Datasource import Datasource
import re

class Bind:
    def __init__(self, id, predicate_name, bind_annotation, datasource: Datasource):
        self.id = id
        self.predicate_name = predicate_name
        self.bind_annotation = bind_annotation
        self.datasource = datasource
        self.database_type = self.get_database_type()
        self.database_alias = self.get_database_alias()

    def to_dict(self):
        return {
            'id': self.id,
            'predicateName': self.predicate_name,
            'bindAnnotation': self.bind_annotation,
            'datasource': self.datasource.to_dict()
        }
    
    def get_datasource(self):
        return self.datasource
    
    def get_database_type(self):
        bind_annotation = self.bind_annotation
        pattern = r'@(?:fakebind)\("([^"]+)","([^"]+)"'
        match = re.search(pattern, bind_annotation)
        if not match:
            return "default type"
        return match.group(1)

    def get_database_alias(self):
        bind_annotation = self.bind_annotation
        pattern = r'@(?:fakebind)\("([^"]+)","([^"]+)"'
        match = re.search(pattern, bind_annotation)
        if not match:
            return "default alias"
        return match.group(2)

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            predicate_name=data['predicateName'],
            bind_annotation=data.get('bindAnnotation'),
            datasource=Datasource.from_dict(data.get('datasource'))
        )
