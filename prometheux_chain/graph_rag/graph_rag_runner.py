# graph_rag_runner.py
from ..client.JarvisPyClient import JarvisPyClient


def graph_rag(question, vada_file_path):
    """
    Function to process the user's question and output the results.

    Parameters:
        question (str): The user's natural language question.
        vada_file_path (str): The path to the .vada file.
    """
    # Read the vadalog program from the file
    try:
        with open(vada_file_path, 'r') as file:
            vadalog_program = file.read()
    except FileNotFoundError:
        print(f"Error: File '{vada_file_path}' not found. Please check the file path.")
        return None
    except Exception as e:
        print(f"Error reading file '{vada_file_path}': {e}")
        return None

    # Initialize the client
    client = JarvisPyClient()

    # Check if JarvisPy is reachable
    if not client.is_reachable():
        print("Error: JarvisPy backend is not reachable.")
        return None

    return client.graph_rag(question, vadalog_program)

