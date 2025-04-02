from typing import Literal, Optional

from langchain_core.language_models.chat_models import BaseChatModel
from pydantic import SecretStr

# Supported LLM providers
LLMProvider = Literal["google", "anthropic", "openai", "mistral"]


def get_llm(
    provider: LLMProvider,
    model_name: Optional[str] = None,
    temperature: float = 0.1,
    api_key: Optional[str] = None,
) -> BaseChatModel:
    """
    Factory function to create a LangChain chat model for the specified provider.

    Args:
        provider: The LLM provider to use
        model_name: Optional model name (if None, uses provider's default)
        temperature: Temperature parameter for the model
        api_key: Optional API key (if None, uses environment variable)

    Returns:
        A LangChain chat model instance

    Raises:
        ValueError: If the provider is not supported or required environment variables are missing
    """
    # Convert API key to SecretStr if provided
    if api_key:
        secret_key = SecretStr(api_key)
        if provider == "google":
            from langchain_google_genai import ChatGoogleGenerativeAI

            return ChatGoogleGenerativeAI(
                model=model_name or "gemini-2.0-flash",
                temperature=temperature,
                api_key=secret_key,
            )

        elif provider == "anthropic":
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic(
                model_name=model_name or "claude-3.5-sonnet-20240620",
                temperature=temperature,
                timeout=None,
                stop=None,
                api_key=secret_key,
            )

        elif provider == "openai":
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=model_name or "gpt-3.5-turbo",
                temperature=temperature,
                api_key=secret_key,
            )

        elif provider == "mistral":
            from langchain_mistralai.chat_models import ChatMistralAI

            return ChatMistralAI(
                model_name=model_name or "mistral-large-latest",
                temperature=temperature,
                api_key=secret_key,
            )
    else:
        if provider == "google":
            from langchain_google_genai import ChatGoogleGenerativeAI

            return ChatGoogleGenerativeAI(
                model=model_name or "gemini-2.0-flash", temperature=temperature
            )

        elif provider == "anthropic":
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic(
                model_name=model_name or "claude-3.5-sonnet-20240620",
                temperature=temperature,
                timeout=None,
                stop=None,
            )

        elif provider == "openai":
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=model_name or "gpt-3.5-turbo", temperature=temperature
            )

        elif provider == "mistral":
            from langchain_mistralai.chat_models import ChatMistralAI

            return ChatMistralAI(
                model_name=model_name or "mistral-large-latest", temperature=temperature
            )

    raise ValueError(f"Unsupported LLM provider: {provider}")
