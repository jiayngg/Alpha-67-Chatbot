from injector import inject

from src.common.config import Config
from src.base.components.embeddings.base import BaseEmbedding as EmbeddingsInterface
from .base import BaseVectorDatabase

@inject
def create_vector_database(config: Config, embeddings: EmbeddingsInterface) -> BaseVectorDatabase:
    """
    Create a vector database based on the type.
    """
    vector_database_type = config.vector_database_type.upper() if config.vector_database_type else None
    if vector_database_type == "CHROMA":
        from .variants.chromadb import ChromaVectorDatabase
        return ChromaVectorDatabase(config, embeddings)
    elif vector_database_type == "INMEM":
        from .variants.inmem import InMemoryVectorDatabase
        return InMemoryVectorDatabase(config, embeddings)
    elif vector_database_type == "SUPABASE":
        from .variants.supabase import SupabaseVectorDatabase
        return SupabaseVectorDatabase(config, embeddings)
    else:
        raise ValueError(f"Invalid vector database type: {vector_database_type}")
