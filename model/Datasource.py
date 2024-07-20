class Datasource:
    def __init__(self, id=None, name="", column_names=None, json_schema="", database_info_id=None):
        self.id = id
        self.name = name
        self.column_names = column_names if column_names is not None else []
        self.json_schema = json_schema
        self.database_info_id = database_info_id

    def get_database_info_id(self):
        return self.database_info_id

    def to_dict(self):
        """Converts the object to a dictionary suitable for JSON serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'columnNames': self.column_names,
            'jsonSchema': self.json_schema,
            'databaseInfoId': self.database_info_id
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a DatasourceDto object from a dictionary."""
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            column_names=data.get('columnNames', []),
            json_schema=data.get('jsonSchema', ""),
            database_info_id=data.get('databaseInfoId')
        )
