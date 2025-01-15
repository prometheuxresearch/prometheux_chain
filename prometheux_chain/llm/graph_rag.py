from ..client.JarvisPyClient import JarvisPyClient

"""
Graph RAG Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def graph_rag(question=None, vadalog_program=None):
    """
    Function to process the user's question and output the results.

    Parameters:
        question (str): The user's natural language question.
        vada_file_path (str): The path to the .vada file.
    """
    if not question and not vadalog_program:
        raise Exception("Please provide a question to ask or a vadalog_program for reasoning or both")
    # Read the vadalog program from the file
    if vadalog_program:
        try:
            with open(vadalog_program, 'r') as file:
                vadalog_program = file.read()
        except FileNotFoundError:
            print(f"Error: File '{vadalog_program}' not found. Please check the file path.")
            return None
        except Exception as e:
            print(f"Error reading file '{vadalog_program}': {e}")
            return None

    # Initialize the client
    client = JarvisPyClient()

    # Check if JarvisPy is reachable
    if not client.is_reachable():
        print("Error: JarvisPy backend is not reachable.")
        return None

    return client.graph_rag(question, vadalog_program)

