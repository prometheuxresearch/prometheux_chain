from ..model.Datasource import Datasource

class Bind:
    def __init__(self, id, predicate_name, bind_annotation, datasource: Datasource):
        self.id = id
        self.predicate_name = predicate_name
        self.bind_annotation = bind_annotation
        self.datasource = datasource

    def to_dict(self):
        return {
            'id': self.id,
            'predicateName': self.predicate_name,
            'bindAnnotation': self.bind_annotation,
            'datasource': self.datasource.to_dict()
        }
    
    def get_datasource(self):
        return self.datasource

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            predicate_name=data['predicateName'],
            bind_annotation=data.get('bindAnnotation'),
            datasource=Datasource.from_dict(data.get('datasource'))
        )
