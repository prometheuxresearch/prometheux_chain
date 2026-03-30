"""
JarvisPy Client Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""

import os
from urllib.parse import quote

import requests

from ..config import config
from ..data.database import Database


class JarvisPyClient:

    @staticmethod
    def _get_auth():
        pmtx_token = os.environ.get('PMTX_TOKEN', config.get('PMTX_TOKEN', ''))
        if not pmtx_token:
            raise Exception("PMTX_TOKEN is not set. Please set it in environment variables or config.")
        return pmtx_token

    @staticmethod
    def _request(method, path, json=None, params=None):
        """Send an authenticated request to the JarvisPy backend."""
        pmtx_token = JarvisPyClient._get_auth()
        url = f"{config['JARVISPY_URL']}{path}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {pmtx_token}"
        }
        response = requests.request(method, url, headers=headers, json=json, params=params)
        return JarvisPyClient._handle_response(response)

    @staticmethod
    def _handle_response(response):
        if response.status_code == 401:
            raise Exception("Unauthorized: Invalid or expired token. Please check your PMTX_TOKEN.")
        elif response.status_code == 403:
            raise Exception("Forbidden: You don't have permission to perform this action.")
        elif response.status_code == 404:
            raise Exception("Not Found: The requested resource was not found.")
        elif response.status_code >= 400:
            raise Exception(f"HTTP Error {response.status_code}: {response.text}")
        try:
            return response.json()
        except ValueError:
            raise Exception(f"Invalid JSON response from server: {response.text}")

    # ── Projects ──────────────────────────────────────────────────────────

    @staticmethod
    def save_project(project_id, project_name, project_scope, description=None):
        payload = {'project': {'id': project_id, 'name': project_name, 'scope': project_scope}}
        if description is not None:
            payload['project']['description'] = description
        return JarvisPyClient._request("POST", "/api/v1/projects/save", json=payload)

    @staticmethod
    def list_projects(project_scopes):
        scopes = ','.join(project_scopes) if isinstance(project_scopes, (list, tuple)) else project_scopes
        return JarvisPyClient._request("GET", "/api/v1/projects/list", params={'scopes': scopes})

    @staticmethod
    def load_project(project_id, project_scope):
        return JarvisPyClient._request("GET", "/api/v1/projects/load",
                                       params={'project_id': project_id, 'scope': project_scope})

    @staticmethod
    def cleanup_projects(project_id, project_scope):
        return JarvisPyClient._request("POST", "/api/v1/projects/cleanup",
                                       json={'project': {'id': project_id, 'scope': project_scope}})

    @staticmethod
    def copy_project(project_id, target_scope="user", new_project_name=None):
        return JarvisPyClient._request("POST", "/api/v1/projects/copy",
                                       json={'project_id': project_id, 'target_scope': target_scope,
                                             'new_project_name': new_project_name})

    @staticmethod
    def export_project(project_id, scope="user"):
        return JarvisPyClient._request("POST", "/api/v1/projects/export-project",
                                       json={'project_id': project_id, 'scope': scope})

    @staticmethod
    def import_project(export_data, scope="user"):
        return JarvisPyClient._request("POST", "/api/v1/projects/import-project",
                                       json={'export_data': export_data, 'scope': scope})

    @staticmethod
    def export_workspace(scope="user"):
        return JarvisPyClient._request("POST", "/api/v1/projects/export-workspace", json={'scope': scope})

    @staticmethod
    def import_workspace(export_data, scope="user"):
        return JarvisPyClient._request("POST", "/api/v1/projects/import-workspace",
                                       json={'export_data': export_data, 'scope': scope})

    # ── Data sources ──────────────────────────────────────────────────────

    @staticmethod
    def cleanup_sources(source_ids):
        return JarvisPyClient._request("POST", "/api/v1/data/cleanup", json={'source_ids': source_ids})

    @staticmethod
    def connect_sources(database_payload: Database, compute_row_count=False):
        return JarvisPyClient._request("POST", "/api/v1/data/connect",
                                       json={'database': database_payload.to_dict(),
                                             'computeRowCount': compute_row_count})

    @staticmethod
    def list_sources():
        return JarvisPyClient._request("GET", "/api/v1/data/list", params={'scope': 'user'})

    @staticmethod
    def infer_schema(database: Database, add_bind: bool, add_model: bool):
        return JarvisPyClient._request("POST", "/api/v1/data/infer-schema",
                                       json={'database': database.to_dict(),
                                             'addBind': add_bind, 'addModel': add_model})

    # ── Concepts ──────────────────────────────────────────────────────────

    @staticmethod
    def save_concept(project_id, code, python_scripts=None, scope="user",
                     description=None, concept_type="logic", concept_name=None,
                     binds=None, output_predicate="", existing_name=None,
                     position=None, group="group_id", compute=None):
        payload = {'code': code, 'scope': scope, 'concept_type': concept_type}
        if python_scripts:
            payload['python_scripts'] = python_scripts
        if description:
            payload['description'] = description
        if concept_name:
            payload['concept_name'] = concept_name
        if binds:
            payload['binds'] = binds
        if output_predicate:
            payload['output_predicate'] = output_predicate
        if existing_name:
            payload['existing_name'] = existing_name
        if position is not None:
            payload['position'] = position
        if group and group != "group_id":
            payload['group'] = group
        if compute:
            payload['compute'] = compute
        return JarvisPyClient._request("POST", f"/api/v1/concepts/{project_id}/save", json=payload)

    @staticmethod
    def run_concept(project_id, concept_name, params=None, scope="user",
                    force_rerun=True, persist_outputs=False, compute=None):
        payload = {
            'params': params or {},
            'force_rerun': force_rerun,
            'persist_outputs': persist_outputs,
            'scope': scope,
        }
        if compute:
            payload['compute'] = compute
        safe_name = quote(concept_name, safe='')
        return JarvisPyClient._request("POST", f"/api/v1/concepts/{project_id}/run/{safe_name}",
                                       json=payload)

    @staticmethod
    def list_concepts(project_id, scope="user"):
        return JarvisPyClient._request("GET", f"/api/v1/concepts/{project_id}/list",
                                       params={'scope': scope})

    @staticmethod
    def cleanup_concepts(project_id, scope="user", concept_names=None):
        payload = {'scope': scope}
        if concept_names:
            payload['concept_names'] = concept_names
        return JarvisPyClient._request("POST", f"/api/v1/concepts/{project_id}/cleanup", json=payload)

    @staticmethod
    def fetch_results(project_id, output_predicate, page=1, page_size=10,
                      scope="user", order_by=None):
        params = {
            'output_predicate': output_predicate,
            'page': page,
            'page_size': page_size,
            'project_scope': scope,
        }
        if order_by:
            params['order_by'] = order_by
        return JarvisPyClient._request("GET", f"/api/v1/concepts/{project_id}/fetch", params=params)

    # ── User config ───────────────────────────────────────────────────────

    @staticmethod
    def save_user_config(config_data, scope="user"):
        return JarvisPyClient._request("POST", "/api/v1/users/save-config",
                                       json={'config_data': config_data, 'scope': scope})

    @staticmethod
    def load_user_config(scope="user"):
        return JarvisPyClient._request("GET", "/api/v1/users/load-config", params={'scope': scope})
