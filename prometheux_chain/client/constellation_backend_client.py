import requests
from ..config import config
from ..model.database import Database

class ConstellationBackendClient:

    @staticmethod
    def infer_schema(database : Database, add_bind: bool, add_model: bool):
        headers = {'Content-Type': 'application/json'}
        payload = {
            "database": database.to_dict(),
            "addBind": add_bind,
            "addModel": add_model
            
        }
        response = requests.post(f"{config['DATA_MANAGER_URL']}/schema-info/infer-schema", headers=headers, json=payload)
        return response
    
    @staticmethod
    def all_pairs_join(databases: list[Database], to_evaluate: bool, parallel: bool):
        # Build the payload as a *native* Python dict—no need to json.dumps this part
        payload = {
            "databasePayloads": [db.to_dict() for db in databases],
            "toEvaluate": to_evaluate,
            "parallel": parallel
        }

        # Use the json= parameter instead of data=
        # requests will automatically serialize `payload` to JSON and set appropriate headers
        response = requests.post(
            f"{config['DATA_MANAGER_URL']}/analysis-info/all-pairs-join",
            json=payload
        )
        return response