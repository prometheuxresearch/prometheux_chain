class SchemaInferencePayload:
    
    def __init__(self, database, username, password, host, port, database_type, table, query, add_bind, options):
        self.database = database
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.databaseType = database_type
        self.addBind = add_bind
        self.options = options
        self.table = table
        self.query = query
    
    def to_dict(self):
        return {
            'database': self.database,
            'username': self.username,
            'password': self.password,
            'host': self.host,
            'port': self.port,
            'databaseType': self.databaseType,
            'addBind': self.addBind,
            'options': self.options,
            'table': self.table,
            'query': self.query
        }
    
    @classmethod
    def from_dict(cls, data):
        schema_inference_payload = cls(
            database=data['database'],
            username="***",
            password="***",
            host=data['host'],
            port=data['port'],
            database_type=data['databaseType'],
            add_bind=data['addBind'],
            options=data['options'],
            table=data['table'],
            query=data['query']
        )
        return schema_inference_payload