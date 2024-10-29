class SchemaInferencePayload:
    def __init__(self, database, username, password, host, port, database_type, add_bind):
        self.database = database
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.databaseType = database_type
        self.addBind = add_bind

    def to_dict(self):
        return {
            'database': self.database,
            'username': self.username,
            'password': self.password,
            'host': self.host,
            'port': self.port,
            'databaseType': self.databaseType,
            'addBind': self.addBind
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
            add_bind=data['addBind']
        )
        return schema_inference_payload
