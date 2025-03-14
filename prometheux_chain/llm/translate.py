import os
import requests

from ..config import config
from ..client.jarvispy_client import JarvisPyClient

"""
Translation Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def translate(domain_knowledge):
    """
    Translate a natural language question into a Vadalog query using the JarvisPy backend.

    :param domain_knowledge: str, the domain_knowledge to be translated.
    :return: str, the translated Vadalog query.
    """
    # Validate the input domain_knowledge
    if not domain_knowledge:
        raise Exception("Please provide a question to translate.")

    # Call the static method to perform the translation
    response = JarvisPyClient.translate(domain_knowledge)

    # Check if the API request was successful
    if response.status_code != 200:
        raise Exception(f"Translation failed with status code {response.status_code}: {response.text}")

    # Extract the translated query from the JSON response.
    # (The key 'vadalog' is assumed; adjust if the actual API returns a different key.)
    vadalog = response.json().get("data", {}).get("vadalog")
    if vadalog is None:
        raise Exception("Translation response does not contain 'vadalog'.")
    return vadalog
