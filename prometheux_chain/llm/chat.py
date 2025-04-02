from ..client.jarvispy_client import JarvisPyClient
import os

"""
Chat Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def chat(text, stream=False):
    chat_response = JarvisPyClient.chat(text, stream=stream)
    if chat_response.status_code != 200:
        return None
       
    # Return the response
    return chat_response.json().get("data", {}).get("answer", "")