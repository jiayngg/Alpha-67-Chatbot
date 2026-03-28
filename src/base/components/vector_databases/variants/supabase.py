from injector import inject
from langchain_postgres import PGVector

from src.common.config import Config
from src.base.components.vector_databases.base import BaseVectorDatabase
from src.base.components.embeddings.base import BaseEmbedding as EmbeddingsInterface


class SupabaseVectorDatabase(BaseVectorDatabase):
    @inject
    def __init__(self, config: Config, embeddings: EmbeddingsInterface):
        super().__init__(embeddings)
        if not config.supabase_postgres_url:
            raise ValueError("Supabase PostgreSQL connection string is not set (SUPABASE_POSTGRES_URL)")

        self.client = PGVector(
            connection=config.supabase_postgres_url,
            embeddings=self.embeddings.embeddings,
            collection_name="documents",
        )
