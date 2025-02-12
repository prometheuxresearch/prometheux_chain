from ..client.jarvispy_client import JarvisPyClient
import os

"""
LLM Output Validation Module

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


def validate(text, guardrail):
    if guardrail is not None:
        if not os.path.exists(guardrail):
            raise Exception(f"Guardrail file '{guardrail}' does not exist.")

        with open(guardrail, 'r', encoding='utf-8') as f:
            guardrail_program = f.read()

        # Call the "validate" API on the guardrail_program
        chat_response = JarvisPyClient.validate(text, guardrail_program)

        # Check if validation was successful
        if chat_response.status_code != 200:
            raise Exception(
                f"Validation error. Detail: {chat_response.json().get('message', 'No message available')}"
            )

        # Parse the response
        validation_data = chat_response.json()["data"]

        # Extract data
        validation_outcome = validation_data["validation_outcome"]
        validation_results = [
            {"outcome": result["outcome"], "explanation": result["explanation"]}
            for result in validation_data["validation_results"]
        ]
        validation_summary = validation_data["validation_summary"]

        # Return structured response
        return {
            "validation_outcome": validation_outcome,
            "validation_results": validation_results,
            "validation_summary": validation_summary
        }

    else:
        raise Exception("Guardrail program must be provided for validation.")
