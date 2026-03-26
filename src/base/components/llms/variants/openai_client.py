"""
OpenAI client module.

This module provides a client for interacting with OpenAI models.
"""

from typing import Dict, Any, Optional, List, Generator, AsyncGenerator

from injector import inject
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

from src.base.components.llms.base import BaseLLMClient
from src.common.config import Config
from src.common.logging import logger


class OpenAIClient(BaseLLMClient):
    """Client for interacting with OpenAI models."""
    @inject
    def __init__(self, config: Config):
        """
        Initialize the OpenAI client.

        Args:
            config: Application configuration
        """
        self.config = config
        self.model_name = config.base_model_name or "gpt-3.5-turbo"
        self.temperature = 0.7
        self.client = ChatOpenAI(
            model=self.model_name,
            api_key=config.openai_api_key,
            temperature=self.temperature,
        )

    def bind_tools(self, tools: Optional[List[Any]] = None) -> None:
        """
        Bind tools to the OpenAI client.
        """
        if tools:
            self.client = self.client.bind_tools([tool.to_openai_tool() for tool in tools])

    def _format_messages(self, messages: List[Dict[str, str]]) -> List[BaseMessage]:
        formatted: List[BaseMessage] = []
        for msg in messages:
            if 'role' in msg and 'content' in msg:
                role, content = msg["role"], msg["content"]
                if role == "user":
                    formatted.append(HumanMessage(content))
                elif role == "assistant":
                    formatted.append(AIMessage(content))
                elif role == "system":
                    formatted.append(SystemMessage(content))
        return formatted

    def chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> Dict[str, Any]:
        """
        Send a chat message to OpenAI and get a response.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            **kwargs: Additional model parameters

        Returns:
            The model's response as a string
        """
        response = self.client.invoke(self._format_messages(messages))
        return {"content": response.content, "additional_kwargs": response.additional_kwargs}

    def stream_chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> Generator[str, None, None]:
        """
        Send a chat message to OpenAI and stream the response.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            **kwargs: Additional model parameters

        Yields:
            Chunks of the response content
        """
        for chunk in self.client.stream(self._format_messages(messages)):
            yield chunk.content

    async def astream_chat(self, messages: List[Dict[str, str]], **kwargs: Any) -> AsyncGenerator[str, None]:
        """
        Send a chat message to OpenAI and stream the response asynchronously.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            **kwargs: Additional model parameters

        Yields:
            Chunks of the response content
        """
        async for chunk in self.client.astream(self._format_messages(messages)):
            yield chunk.content

    def complete(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Send a completion prompt to OpenAI and get a response.
        
        Args:
            prompt: The text prompt to complete
            **kwargs: Additional model parameters
            
        Returns:
            The model's completion as a string
        """
        # For OpenAI, we'll use the chat completions API with a user message
        messages = [{"role": "user", "content": prompt}]
        return self.chat(messages, **kwargs)
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the OpenAI model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "provider": "OpenAI",
            "model": self.model_name,
            "temperature": self.temperature,
        }
    
    def create_chat_model(self, model_kwargs: Optional[Dict[str, Any]] = None) -> ChatOpenAI:
        """
        Create a ChatOpenAI model instance from LangChain.
        
        Args:
            model_kwargs: Model parameters
            
        Returns:
            ChatOpenAI instance
        """
        kwargs = model_kwargs or {}
        
        # Set default parameters
        default_params = {
            "model_name": self.model_name,
            "temperature": self.temperature,
        }
        
        # Override defaults with provided kwargs
        for key, value in default_params.items():
            if key not in kwargs:
                kwargs[key] = value
        
        # Create the model
        return ChatOpenAI(**kwargs)
    
    def close(self) -> None:
        """Close any open resources."""
        # No resources to close for OpenAI client
        pass 