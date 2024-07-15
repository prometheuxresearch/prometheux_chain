class DatabaseInfo:
    def __init__(self, alias, database, username, password, host, port, database_type, connection_status=None):
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

    def __str__(self):
        return f"DatabaseInfo(alias={self.alias}, database={self.database}, username={self.username}, host={self.host}, port={self.port}, database_type={self.databaseType}, connection_status={self.connectionStatus})"
