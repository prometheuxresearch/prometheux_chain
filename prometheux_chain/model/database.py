class Database:
    
    def __init__(self, database_type, username, password, host, port, database_name, tables=None, schema=None, catalog=None, query=None, options=None):
        self.database_type = database_type
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name
        self.options = options
        self.tables = tables
        self.schema = schema
        self.catalog = catalog
        self.query = query
    
    def to_dict(self):
        return {
            'databaseType': self.database_type,
            'username': self.username,
            'password': self.password,
            'host': self.host,
            'port': self.port,
            'databaseName': self.database_name,
            'options': self.options,
            'tables': self.tables,
            'schema': self.schema,
            'catalog': self.catalog,
            'query': self.query
        }
    
    @classmethod
    def from_dict(cls, data):
        schema_inference_payload = cls(
            database_name=data['databaseName'],
            username="***",
            password="***",
            host=data['host'],
            port=data['port'],
            database_type=data['databaseType'],
            options=data['options'],
            tables=data['tables'],
            schema=data['schema'],
            catalog=data['catalog'],
            query=data['query']
        )
        return schema_inference_payload