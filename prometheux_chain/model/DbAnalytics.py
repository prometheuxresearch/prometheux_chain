class DbAnalytics:
    def __init__(self, database_type, username, password, host, port, database, limit):
        self.database = database
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.databaseType = database_type
        self.limit = limit

    def to_dict(self):
        return {
            'database': self.database,
            'username': self.username,
            'password': self.password,
            'host': self.host,
            'port': self.port,
            'databaseType': self.databaseType,
            'limit': self.limit
        }
        

    @classmethod
    def from_dict(cls, data):
        dbAnalytics = cls(
            database=data['database'],
            username="***",
            password="***",
            host=data['host'],
            port=data['port'],
            database_type=data['databaseType'],
            limit=data['limit']
        )
        return dbAnalytics
