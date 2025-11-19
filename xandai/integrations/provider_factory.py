"""
LLM Provider Factory

Creates Ollama provider for offline-only operation.
"""

import os
from typing import List, Optional

from .base_provider import LLMConfig, LLMProvider, ProviderType
from .ollama_provider import OllamaProvider


class LLMProviderFactory:
    """
    Factory for creating Ollama LLM provider
    
    Handles provider instantiation and configuration for offline-only operation.
    """

    @staticmethod
    def create_provider(
        provider_type: str = "ollama",
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        **config_options,
    ) -> LLMProvider:
        """
        Create an Ollama LLM provider

        Args:
            provider_type: Must be "ollama" (for backward compatibility)
            base_url: Ollama endpoint URL
            model: Initial model to use
            **config_options: Additional configuration options

        Returns:
            Configured Ollama provider instance

        Raises:
            ValueError: If provider_type is not "ollama"
        """

        # Normalize and validate provider type
        provider_type = provider_type.lower().strip()

        if provider_type in ["ollama", "ol"]:
            return LLMProviderFactory._create_ollama_provider(base_url, model, **config_options)
        else:
            raise ValueError(
                f"Unsupported provider type: '{provider_type}'. "
                f"Only Ollama is supported for offline operation."
            )

    @staticmethod
    def _create_ollama_provider(
        base_url: Optional[str] = None, model: Optional[str] = None, **config_options
    ) -> OllamaProvider:
        """Create Ollama provider with environment variable support"""

        # Use defaults from environment or sensible defaults
        if base_url is None:
            base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")

        if model is None:
            model = os.getenv("XANDAI_MODEL", None)  # Don't assume a default model

        # Create configuration with defaults and overrides
        config = LLMConfig(
            provider_type=ProviderType.OLLAMA,
            base_url=base_url,
            model=model,
            temperature=config_options.get("temperature", 0.7),
            top_p=config_options.get("top_p", 0.9),
            max_tokens=config_options.get("max_tokens", 2048),
            context_length=config_options.get("context_length", 4096),
            timeout=config_options.get("timeout", 120),
            extra_options=config_options.get("extra_options", {}),
        )

        return OllamaProvider(config)

    @staticmethod
    def create_from_env() -> LLMProvider:
        """Create Ollama provider based on environment variables only"""

        base_url = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        model = os.getenv("XANDAI_MODEL", None)

        # Additional environment-based configuration
        config_options = {}

        # Parse temperature from env
        temp_str = os.getenv("XANDAI_TEMPERATURE", "0.7")
        try:
            config_options["temperature"] = float(temp_str)
        except ValueError:
            config_options["temperature"] = 0.7

        # Parse max tokens from env
        max_tokens_str = os.getenv("XANDAI_MAX_TOKENS", "2048")
        try:
            config_options["max_tokens"] = int(max_tokens_str)
        except ValueError:
            config_options["max_tokens"] = 2048

        return LLMProviderFactory.create_provider(
            provider_type="ollama",
            base_url=base_url,
            model=model,
            **config_options,
        )

    @staticmethod
    def get_supported_providers() -> List[str]:
        """Get list of supported provider types (Ollama only)"""
        return ["ollama"]

    @staticmethod
    def create_auto_detect(
        preferred_provider: Optional[str] = None, fallback_provider: str = "ollama"
    ) -> LLMProvider:
        """
        Create Ollama provider (for backward compatibility)

        Args:
            preferred_provider: Ignored (always uses Ollama)
            fallback_provider: Ignored (always uses Ollama)

        Returns:
            Ollama provider instance
        """
        return LLMProviderFactory.create_provider("ollama")
