from typing import Optional
import openai

from ..llm.llm_manager import LLMManager

"""
XXXXX

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


class OpenAIManager(LLMManager):
    """
    Concrete LLM Manager for OpenAI.
    """

    def __init__(self, llm_api_key: Optional[str], llm_version: str,
                 llm_temperature: float, llm_max_tokens: int):
        super().__init__(
            llm_api_key=llm_api_key,
            llm_version=llm_version,
            llm_temperature=llm_temperature,
            llm_max_tokens=llm_max_tokens
        )
        if not self.llm_api_key:
            raise ValueError("OpenAI API Key is required.")
        # Set the API key globally for the OpenAI client
        openai.api_key = self.llm_api_key

    def send_request(self, system_prompt: str, user_prompt: str) -> str:
        """
        Sends a prompt to OpenAI's ChatCompletion API and returns the raw text response.
        """
        try:
            response = openai.chat.completions.create(
                model=self.llm_version,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.llm_temperature,
                max_tokens=self.llm_max_tokens
            )
        except Exception as e:
            raise RuntimeError(f"OpenAI API request failed: {str(e)}")

        completion_message = response.choices[0].message.content

        # Remove code fences if present
        if completion_message.startswith("```json"):
            completion_message = completion_message.strip("```json").strip("```")
        elif completion_message.startswith("```"):
            completion_message = completion_message.strip("```")

        return completion_message.strip()
