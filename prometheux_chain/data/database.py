"""
Database Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


class Database:
    
    def __init__(self, database_type, username=None, password=None, host=None, port=None, database_name=None, tables=None, schema=None, catalog=None, query=None, options=None, selected_columns=None, ignore_columns=None, ignore_tables=None, url=None):
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
        self.selected_columns = selected_columns
        self.ignore_columns = ignore_columns
        self.ignore_tables = ignore_tables
        self.url = url
 
    def to_dict(self):
        return {
            'databaseType': self.database_type,
            'username': self.username,
            'password': self.password,
            'host': self.host,
            'port': self.port,
            'databaseName': self.database_name,
            'options': self.options,
            'schema': self.schema,
            'catalog': self.catalog,
            'query': self.query,
            'selectedColumns': self.selected_columns,
            'ignoreColumns': self.ignore_columns,
            'ignoreTables': self.ignore_tables,
            'tables': self.tables,
            'url': self.url
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
            query=data['query'],
            selected_columns=data['selectedColumns'],
            ignore_columns=data['ignoreColumns'],
            ignore_tables=data['ignoreTables'],
            url=data['url']
        )
        return schema_inference_payload