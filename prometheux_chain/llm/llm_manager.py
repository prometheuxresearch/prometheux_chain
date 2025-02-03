from abc import ABC, abstractmethod
from typing import Optional

"""
XXXXX

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


class LLMManager(ABC):
    """
    Abstract base class for LLM Managers.
    Each concrete subclass (e.g., OpenAIManager) must implement `send_request`.
    """

    def __init__(
            self,
            llm_api_key: Optional[str],
            llm_version: str,
            llm_temperature: float,
            llm_max_tokens: int
    ):
        self.llm_api_key = llm_api_key
        self.llm_version = llm_version
        self.llm_temperature = float(llm_temperature)
        self.llm_max_tokens = int(llm_max_tokens)

    @abstractmethod
    def send_request(self, system_prompt: str, user_prompt: str) -> str:
        """
        Sends a prompt to the LLM provider and returns the raw response string.
        Subclasses must implement this method.
        """
        pass
