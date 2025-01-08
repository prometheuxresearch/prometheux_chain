from ..client.JarvisPyClient import JarvisPyClient
import os


def chat(text, guardrail=None):
    # Update LLM configs before any requests FIXME: maybe do this instead of passing to the validate the configs
    #JarvisPyClient.update_llm_configs()

    chat_response = None

    # If guardrail path is provided, read its contents and call the new backend "validate" API
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

    else:
        # Else proceed with the normal chat request (example calls queryExplain)
        # chat_response = JarvisPyClient.queryExplain(text)
        # if chat_response.status_code != 200:
        #    raise Exception(f"Chat error. Detail: {chat_response.json()['message']}")
        pass

    return chat_response.json()["data"]
