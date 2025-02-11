import time
import warnings

from ..client.jarvispy_client import JarvisPyClient
from ..llm.llm_manager import LLMManager
from ..llm.openai_manager import OpenAIManager
from ..config import config

"""
Reasoning-Augmented Generation Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def rag(question, virtual_kg, measure_time=False, to_explain=False):
    """
    Function to process the user's question and output the results.
    """
    # Check if JarvisPy is reachable
    if not JarvisPyClient.is_reachable():
        raise Exception("Error: JarvisPy backend is not reachable.")

    if not question or not virtual_kg:
        raise Exception("Please provide a question and a virtual knowledge graph.")

    # Check parameters compatibility
    if not to_explain:
        warnings.warn("RAG will be slower but more effective if to_explain is set to True.")

    # Measure time if needed
    start_time = time.time() if measure_time else None

    # Call JarvisPyClient
    response = JarvisPyClient.rag(
        question=question,
        virtual_kg=virtual_kg,
        to_explain=to_explain
    )

    # Print timing info if needed
    if measure_time:
        elapsed_time = time.time() - start_time
        print(f"RAG completed in {elapsed_time:.2f} seconds.")

    # Extract the context from the RAG response
    rag_result = response.json().get("data", {}).get("output_facts_and_explanations", {})
    facts_explanations_only = []
    for item in rag_result:
        facts_explanations_only.append({
            "fact": item.get("fact"),
            "textual_explanation": item.get("textual_explanation")
        })

    # TODO: handle "structured_explanation" (JSON) for better visualization if needed

    # Call the chat function
    chat_response = JarvisPyClient.chat(question, facts_explanations_only)
    if chat_response.status_code != 200:
        return None
    
    # Return the response
    return chat_response.json().get("data", {}).get("answer", "")
