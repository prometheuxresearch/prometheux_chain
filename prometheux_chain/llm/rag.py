from ..client.jarvispy_client import JarvisPyClient

"""
Reasoning-Augmented Generation Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def rag(question=None, vadalog_program=None):
    """
    Function to process the user's question and output the results.

    Parameters:
        question (str): The user's natural language question.
        vadalog_program (str): The path to the .vada file.
    """
    # Check if JarvisPy is reachable
    if not JarvisPyClient.is_reachable():
        print("Error: JarvisPy backend is not reachable.")
        return None

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

    return JarvisPyClient.rag(question, vadalog_program)

