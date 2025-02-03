import time
import json

from ..client.jarvispy_client import JarvisPyClient
from ..common.vadalog_utils import process_vadalog_files
from ..llm.llm_manager import LLMManager
from ..llm.openai_manager import OpenAIManager
from ..config import config

"""
Reasoning-Augmented Generation Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def rag(question, virtual_kg, vadalog_params=None, measure_time=False, to_explain=True, to_persist=True):
    """
    Function to process the user's question and output the results.
    """
    # Check if JarvisPy is reachable
    if not JarvisPyClient.is_reachable():
        print("Error: JarvisPy backend is not reachable.")
        return None

    if not question or not virtual_kg:
        raise Exception("Please provide a question and a virtual knowledge graph.")

    # Process vadalog files into the structured format
    vadalog_programs = process_vadalog_files(virtual_kg)

    # Measure time if needed
    start_time = time.time() if measure_time else None

    # Call JarvisPyClient
    response = JarvisPyClient.rag(
        question=question,
        vadalog_programs=vadalog_programs,
        vadalog_params=vadalog_params,
        to_explain=to_explain,
        to_persist=to_persist
    )

    # Print timing info if needed
    if measure_time:
        elapsed_time = time.time() - start_time
        print(f"RAG completed in {elapsed_time:.2f} seconds.")

    # Extract the context from the RAG response
    rag_result = response.json()
    context = ""
    output_facts = rag_result.get("data", {}).get("output_facts", {})
    context = json.dumps(output_facts, indent=2)
    
    # Initialize the LLM manager
    llm_manager: LLMManager = OpenAIManager(
            llm_api_key=config.get("LLM_API_KEY"),
            llm_version=config.get("LLM_VERSION"),
            llm_temperature=config.get("LLM_TEMPERATURE"),
            llm_max_tokens=config.get("LLM_MAX_TOKENS")
    )

    # Build the system prompt
    system_prompt = f"""
    You are a helpful assistant. Your job is to answer questions based on the provided context.
    If the context does not contain the answer, you must say "I am sorry, I do not know the answer to that question. Do not refer explicitly to having received the context."
    """

    # Build the user prompt
    user_prompt = f"""
    Answer the following question based on the provided context.
    Question: {question}
    Context: {context}
    """
    
    # Call the LLM manager to generate the response
    response = llm_manager.send_request(system_prompt, user_prompt)

    return response
