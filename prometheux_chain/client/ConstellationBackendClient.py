import requests
import json
from ..config import config
from ..model.DatabaseInfo import DatabaseInfo
from ..model.SchemaInferencePayload import SchemaInferencePayload
from ..model.DbAnalytics import DbAnalytics

class ConstellationBackendClient:
    @staticmethod
    def store_database_info(database_info : DatabaseInfo):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(database_info.to_dict())
        response = requests.post(f"{config['CONSTELLATION_BACKEND_URL']}/database-info/store", headers=headers, data=data)
        return response
    
    @staticmethod
    def vadalog_db_analytics(db_analytics_payload : list[DbAnalytics]):
        headers = {'Content-Type': 'application/json'}
        data = []
        for db_analytics in db_analytics_payload:
            data.append(db_analytics.to_dict())
        response = requests.post(f"{config['CONSTELLATION_BACKEND_URL']}/analytics-info/vadalog-dbanalytics", headers=headers, json=data)
        return response
    
    @staticmethod
    def infer_from_schema(schema_inference_payload : SchemaInferencePayload):
        headers = {'Content-Type': 'application/json'}
        data = json.dumps(schema_inference_payload.to_dict())
        response = requests.post(f"{config['CONSTELLATION_BACKEND_URL']}/schema-info/inferFromSchema", headers=headers, data=data)
        return response

    @staticmethod
    def get_datasources_by_database(database_id=None, database_alias=None):
        headers = {'Content-Type': 'application/json'}
        params = {}
        if database_id:
            params['databaseId'] = database_id
        if database_alias:
            params['databaseAlias'] = database_alias

        response = requests.get(f"{config['CONSTELLATION_BACKEND_URL']}/datasource-info/getByDatabase", headers=headers, params=params)
        return response


    @staticmethod
    def get_all_databases():
        headers = {'Content-Type': 'application/json'}
        response = requests.get(f"{config['CONSTELLATION_BACKEND_URL']}/database-info/all", headers=headers)
        return response
    
    @staticmethod
    def delete_all_databases():
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(f"{config['CONSTELLATION_BACKEND_URL']}/database-info/deleteAll", headers=headers)
        return response