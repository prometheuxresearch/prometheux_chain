from typing import Optional

from .llm_manager import LLMManager
from .openai_manager import OpenAIManager
# from .anthropic_manager import AnthropicManager   # example for future expansion
# from .azure_manager import AzureManager           # example for future expansion

"""
XXXXX

Copyright (C) Prometheux Limited. All rights reserved.

Author: Prometheux Limited
"""


class LLMFactory:
    """
    Returns an LLM Manager object corresponding to the specified provider.
    Currently supports OpenAI by default. Extend as needed for other providers.
    """

    def create_llm_manager(
            self,
            llm_provider: Optional[str],
            llm_api_key: Optional[str],
            llm_version: str,
            llm_temperature: float,
            llm_max_tokens: int
    ) -> LLMManager:
        """
        Create and return an LLM manager based on `provider`.
        If provider is not specified or recognized, raise an error or default to OpenAI.
        """
        # Convert provider to lowercase, handle None
        provider = (llm_provider or "").lower()

        if provider in ["openai", ""]:
            return OpenAIManager(
                llm_api_key=llm_api_key,
                llm_version=llm_version,
                llm_temperature=llm_temperature,
                llm_max_tokens=llm_max_tokens
            )

        # Add logic for other LLM managers here:
        # elif provider == "anthropic":
        #     return AnthropicManager(api_key, provider, model_version, max_tokens)
        # elif provider == "azure":
        #     return AzureManager(api_key, provider, model_version, max_tokens)
        # else:
        #     raise ValueError(f"Unsupported LLM provider: {provider}")

        raise ValueError(f"Unsupported LLM provider: {provider}")
