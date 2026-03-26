from injector import inject
from supabase import create_client
from langchain_community.vectorstores import SupabaseVectorStore

from src.common.config import Config
from src.base.components.vector_databases.base import BaseVectorDatabase
from src.base.components.embeddings.base import BaseEmbedding as EmbeddingsInterface


class SupabaseVectorDatabase(BaseVectorDatabase):
    @inject
    def __init__(self, config: Config, embeddings: EmbeddingsInterface):
        super().__init__(embeddings)
        if not config.supabase_url:
            raise ValueError("Supabase URL is not set")
        if not config.supabase_service_key:
            raise ValueError("Supabase service key is not set")

        supabase_client = create_client(config.supabase_url, config.supabase_service_key)
        self.client = SupabaseVectorStore(
            client=supabase_client,
            embedding=self.embeddings.embeddings,
            table_name="documents",
            query_name="match_documents",
        )
