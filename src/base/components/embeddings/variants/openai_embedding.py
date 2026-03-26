from typing import List

from injector import inject
from pydantic import SecretStr
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from src.base.components.embeddings.base import BaseEmbedding
from src.common.config import Config


class OpenAIEmbedding(BaseEmbedding):
    @inject
    def __init__(self, config: Config):
        super().__init__(config)
        if not config.openai_api_key:
            raise ValueError("OpenAI API key is not set")

        self.embeddings = OpenAIEmbeddings(
            api_key=SecretStr(config.openai_api_key),
            model=config.openai_embedding_model,
        )

    def process(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)

    def process_documents(self, documents: List[Document]) -> List[List[float]]:
        return self.embeddings.embed_documents([doc.page_content for doc in documents])

    async def aprocess_documents(self, documents: List[Document]) -> List[List[float]]:
        return await self.embeddings.aembed_documents([doc.page_content for doc in documents])
