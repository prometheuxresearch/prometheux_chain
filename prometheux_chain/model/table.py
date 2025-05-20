from column import Column

class Table:
    def __init__(self, name: str, schema: str=None, columns: list[Column]=None):
        self.name = name
        self.schema = schema
        self.columns = columns

    def to_dict(self):
        return {
            "name": self.name,
            "schema": self.schema,
            "columns": [column.to_dict() for column in self.columns]
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["schema"], [Column.from_dict(column) for column in data["columns"]])

