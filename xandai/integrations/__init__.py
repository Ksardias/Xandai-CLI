"""
XandAI Integrations - Ollama integration for offline AI

Provides unified interface for Ollama LLM provider through standardized abstractions.
"""

from .base_provider import LLMConfig, LLMProvider, LLMResponse, ProviderType

# Legacy compatibility - maintain existing imports
from .ollama_client import OllamaClient, OllamaResponse
from .ollama_provider import OllamaProvider
from .provider_factory import LLMProviderFactory

__all__ = [
    # New provider system
    "LLMProvider",
    "LLMResponse",
    "LLMConfig",
    "ProviderType",
    "OllamaProvider",
    "LLMProviderFactory",
    # Legacy compatibility
    "OllamaClient",
    "OllamaResponse",
]
