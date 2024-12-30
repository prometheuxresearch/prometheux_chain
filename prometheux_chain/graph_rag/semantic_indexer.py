from ..client.JarvisPyClient import JarvisPyClient


def semantic_indexing(vada_file_path):
    """
    Function to perform semantic indexing by reading a .vada file,
    sending it to JarvisPy backend, and handling responses.

    Parameters:
        vada_file_path (str): The path to the .vada file.
    """
    # Read the .vada file as a string
    try:
        with open(vada_file_path, 'r') as file:
            vadalog_program = file.read()
    except FileNotFoundError:
        return f"Error: File '{vada_file_path}' not found. Please check the file path."
    except Exception as e:
        return f"Error reading file '{vada_file_path}': {e}"

    # Initialize the JarvisPyClient
    client = JarvisPyClient()

    # Check if JarvisPy backend is reachable
#    if not client.is_reachable():
#        return "Error: JarvisPy backend is not reachable. Ensure the backend is running and accessible."

    return client.semantic_indexing(vadalog_program)

