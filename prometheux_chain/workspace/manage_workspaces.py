from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Workspace Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def export_workspace(workspace_id="workspace_id", scope="user"):
    """
    Export all tables from a workspace.
    
    Args:
        workspace_id (str): The ID of the workspace to export (default: "workspace_id")
        scope (str): The scope of the export (default: "user")
    
    Returns:
        dict: Response containing exported table data with the following structure:
        {
            "status": "success",
            "message": "Workspace tables exported successfully...",
            "data": {
                "workspace_id": "your_workspace_id",
                "scope": "user",
                "extraction_timestamp": "2024-01-15T10:30:00.000Z",
                "database_info": {...},
                "workspace_level_tables": [...],
                "project_tables": [...],
                "tables": {...},
                "summary": {...}
            }
        }
    
    Raises:
        Exception: If the export fails or returns an error status
    """
    response = JarvisPyClient.export_workspace(workspace_id=workspace_id, scope=scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during exporting workspace tables: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {})
    else:
        raise Exception(f"An exception occurred during exporting workspace tables: {response.get('message', 'Unknown error')}")


def import_workspace(export_data, workspace_id="workspace_id", scope="user"):
    """
    Import tables into a workspace from exported data.
    
    Args:
        export_data (dict): The complete export data from the export endpoint
        workspace_id (str): The ID of the target workspace (default: "workspace_id")
        scope (str): The target scope for the import (default: "user")
    
    Returns:
        dict: Response containing import status:
        {
            "status": "success",
            "message": "Workspace tables imported successfully"
        }
    
    Raises:
        Exception: If the import fails or returns an error status
        ValueError: If export_data is missing or invalid
    """
    if not export_data:
        raise ValueError("export_data is required and cannot be empty")
    
    if not isinstance(export_data, dict):
        raise ValueError("export_data must be a dictionary")
    
    response = JarvisPyClient.import_workspace(export_data=export_data, workspace_id=workspace_id, scope=scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during importing workspace tables: {msg}")
    
    if response.get('status') == 'success':
        return response
    else:
        raise Exception(f"An exception occurred during importing workspace tables: {response.get('message', 'Unknown error')}")
