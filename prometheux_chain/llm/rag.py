import time
import warnings

from ..client.jarvispy_client import JarvisPyClient
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
    response_json = response.json()
    data_block = response_json.get("data", {})

    output_facts_and_explanations = data_block.get("output_facts_and_explanations", [])
    translated_question_rules = data_block.get("translated_question_rules", "")
    top_retrieved_facts = data_block.get("top_retrieved_facts", "")
    predicates_and_models = data_block.get("predicates_and_models", "")

    # Build just the minimal "facts_and_explanations" structure for the chat call
    facts_explanations_only = []
    for item in output_facts_and_explanations:
        facts_explanations_only.append({
            "fact": item.get("fact"),
            "textual_explanation": item.get("textual_explanation")
        })


    # TODO: handle "structured_explanation" (JSON) for better visualization if needed

    # Call the chat function
    chat_response = JarvisPyClient.chat(
        question=question,
        facts_and_explanations=facts_explanations_only,
        translated_question_rules=translated_question_rules,
        top_retrieved_facts=top_retrieved_facts,
        predicates_and_models=predicates_and_models,
        to_explain=to_explain
    )

    if chat_response.status_code != 200:
        return None
    
    # Return the response
    return chat_response.json().get("data", {}).get("answer", "")
