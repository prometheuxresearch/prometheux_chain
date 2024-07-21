class DatabaseInfo:
    def __init__(self, id, alias, database, username, password, host, port, database_type, connection_status=None):
        self.id = id
        self.alias = alias
        self.database = database
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.databaseType = database_type
        self.connectionStatus = connection_status

    def to_dict(self):
        return {
            'alias': self.alias,
            'database': self.database,
            'username': self.username,
            'password': self.password,
            'host': self.host,
            'port': self.port,
            'databaseType': self.databaseType,
            'connectionStatus': self.connectionStatus
        }
        

    @classmethod
    def from_dict(cls, data):
        database_info = cls(
            id=data['id'],
            alias=data['alias'],
            database=data['database'],
            username="***",
            password="***",
            host=data['host'],
            port=data['port'],
            database_type=data['databaseType'],
            connection_status=data['connectionStatus']
        )
        return database_info
