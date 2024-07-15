import yaml
from ..client.ConstellationBackendClient import ConstellationBackendClient
from ..model.DatabaseInfo import DatabaseInfo

def connect_from_yaml(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    databases = []

    for db_config in config['databases']:
        db_info = DatabaseInfo(
            alias=db_config['alias'],
            database=db_config['database'],
            username=db_config['username'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port'],
            database_type=db_config['database_type']
        )
        stored_data = ConstellationBackendClient.store_database_info(db_info)
        db_info.connection_status = "Connected" if stored_data else "Failed"
        databases.append(db_info)

    return databases
