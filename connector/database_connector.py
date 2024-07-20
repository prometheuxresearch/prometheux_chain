import yaml
from ..client.ConstellationBackendClient import ConstellationBackendClient
from ..model.DatabaseInfo import DatabaseInfo

def connect_from_yaml(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    
    databases = []

    for db_config in config['databases']:
        db_info = DatabaseInfo(
            id = None,
            alias=db_config['alias'],
            database=db_config['database'],
            username=db_config['username'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port'],
            database_type=db_config['database_type']
        )
        store_response = ConstellationBackendClient.store_database_info(db_info)
        # 409 means conflict: a database having that alias already exists
        if store_response.status_code == 409:
            print(store_response.json()["message"])
        elif store_response.status_code != 200:
            raise Exception(f"HTTP error! status: {store_response.status_code}, detail: {store_response.json().message}")
        if store_response.status_code == 200:
            store_response.json()["message"]

    get_all_response = ConstellationBackendClient.get_all_databases()
    if get_all_response.status_code != 200:
        raise Exception(f"HTTP error! status: {get_all_response.status_code}, detail: {get_all_response.json().message}")
    get_databases = get_all_response.json()["data"]
    databases = []
    for get_db in get_databases:
        db_info = DatabaseInfo.from_dict(get_db)
        databases.append(db_info)
    return databases
