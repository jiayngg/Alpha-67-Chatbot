from src.common.config import Config
from .variants.azure_openai_embedding import AzureOpenAIEmbedding
from .variants.openai_embedding import OpenAIEmbedding
from .base import BaseEmbedding


def create_embedding(config: Config) -> BaseEmbedding:
    embedding_type = config.embedding_type.upper() if config.embedding_type else None
    if embedding_type == "AZUREOPENAI":
        return AzureOpenAIEmbedding(config)
    elif embedding_type == "OPENAI":
        return OpenAIEmbedding(config)
    else:
        raise ValueError(f"Embedding type {embedding_type} not supported")
