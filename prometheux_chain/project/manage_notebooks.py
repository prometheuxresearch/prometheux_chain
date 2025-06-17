from prometheux_chain.client.jarvispy_client import JarvisPyClient

"""
Notebook Management Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def cleanup_notebooks(project_id, project_scope="user", notebook_ids=None):
    """
    Cleanup notebooks for a specific project.
    If `notebook_ids` is provided, it only cleans up those specific notebooks.
    If `notebook_ids` is None, it cleans up all notebooks for the project.
    """
    response = JarvisPyClient.cleanup_notebooks(project_id, project_scope, notebook_ids)

    print(response)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while cleaning up notebooks: {msg}")
    
    if response.get('status') == 'success':
        print(response.get('message', 'Notebooks cleaned up successfully'))
    else:
        raise Exception(f"An exception occurred while cleaning up notebooks: {response.get('message', 'Unknown error')}")


def save_notebook(project_id, project_scope="user", notebook_name=None, notebook_id = None):
    """
    Save a notebook for a specific project.
    Returns the notebook_id of the saved notebook.
    """
    response = JarvisPyClient.save_notebook(project_id, project_scope, notebook_id, notebook_name)

    print(response)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while saving notebook: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {}).get('id')
    else:
        raise Exception(f"An exception occurred while saving notebook: {response.get('message', 'Unknown error')}")


def list_notebooks(project_id, project_scope="user"):
    """
    List all notebooks for a specific project.
    """
    response = JarvisPyClient.list_notebooks(project_id, project_scope)

    print(response)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during loading notebooks: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', [])
    else:
        raise Exception(f"An exception occurred during loading notebooks: {response.get('message', 'Unknown error')}")
    

def load_notebook(project_id, notebook_id, project_scope="user"):
    """
    Load a specific notebook for a specific project.
    """
    response = JarvisPyClient.load_notebook(project_id, notebook_id, project_scope)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during loading notebook: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {})
    else:
        raise Exception(f"An exception occurred during loading notebook: {response.get('message', 'Unknown error')}")


def cleanup_cells(project_id, notebook_id, project_scope="user", cell_ids=None):
    """
    Cleanup cells for a specific notebook.
    If `cell_ids` is provided, it only cleans up those specific cells.
    If `notebook_id` is provided but `cell_ids` is None, it cleans up all cells for that notebook.
    """
    response = JarvisPyClient.cleanup_cells(project_id, project_scope, notebook_id, cell_ids)

    print(response)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while cleaning up cells: {msg}")
    
    if response.get('status') == 'success':
        print(response.get('message', 'Cells cleaned up successfully'))
    else:
        raise Exception(f"An exception occurred while cleaning up cells: {response.get('message', 'Unknown error')}")


def save_cell(project_id, project_scope, notebook_id, cell_content, cell_position=1, cell_id=None):
    """
    Save a cell for a specific notebook.
    Returns the cell_id of the saved cell.
    """
    response = JarvisPyClient.save_cell(project_id, project_scope, notebook_id, cell_content, cell_position, cell_id)

    print(response)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while saving cell: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {}).get('id')
    else:
        raise Exception(f"An exception occurred while saving cell: {response.get('message', 'Unknown error')}")


def run_cell(project_id, notebook_id, project_scope, cell_content, cell_position=1, cell_id=None):
    """
    Execute a cell in a notebook.
    Returns the cell_id of the executed cell.
    """
    response = JarvisPyClient.run_cell(project_id, notebook_id, project_scope, cell_content, cell_position, cell_id)

    print(response)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while executing cell: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {})
    else:
        raise Exception(f"An exception occurred while executing cell: {response.get('message', 'Unknown error')}")


def list_cells(project_id, notebook_id, project_scope="user"):
    """
    List all cells for a specific notebook.
    """
    response = JarvisPyClient.list_cells(project_id, project_scope, notebook_id)

    print(response)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred during listing cells: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', [])
    else:
        raise Exception(f"An exception occurred during listing cells: {response.get('message', 'Unknown error')}")


def list_cell_outputs(project_id, notebook_id, cell_id, output_predicate, project_scope="user", page=1):
    """
    Retrieve output facts from a specific cell in a notebook.
    
    Args:
        project_id (str): The ID of the project
        notebook_id (str): The ID of the notebook
        cell_id (str): The ID of the cell
        output_predicate (str): The predicate to filter output facts
        project_scope (str, optional): The project scope. Defaults to "user".
        
    Returns:
        The output facts from the cell
    """
    response = JarvisPyClient.list_cell_outputs(project_id, project_scope, notebook_id, cell_id, output_predicate, page)

    print(response)

    if response.get('status') != 'success':
        msg = response.get('message', 'Unknown error')
        raise Exception(f"An exception occurred while retrieving cell output facts: {msg}")
    
    if response.get('status') == 'success':
        return response.get('data', {})
    else:
        raise Exception(f"An exception occurred while retrieving cell output facts: {response.get('message', 'Unknown error')}")







