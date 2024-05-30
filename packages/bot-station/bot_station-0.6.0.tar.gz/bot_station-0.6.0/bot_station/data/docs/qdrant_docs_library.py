import logging
from typing import List, Iterable

from qdrant_client import QdrantClient
from qdrant_client.fastembed_common import QueryResponse

from bot_station.data.docs.mapper.document_mapper import DocumentMapper, SOURCE_LINK_KEY
from bot_station.data.bot.model.qdrant_config import QdrantConfig
from bot_station.data.docs.qdrant_docs_iterator import QdrantDocsIterable
from bot_station.domain.docs.docs_library import DocsLibrary
from bot_station.domain.docs.model.document import Document, DocId


class QdrantDocsLibrary(DocsLibrary):
    qdrant_config: QdrantConfig
    collection_name: str

    qdrant_cli: QdrantClient

    __is_loaded: bool

    relevant_docs_limit = 3
    relevant_docs_min_score = 0.7

    def __init__(
            self,
            collection_name: str,
            qdrant_config: QdrantConfig,
    ):
        logging.debug(f"Init {collection_name}")
        self.qdrant_config = qdrant_config
        self.collection_name = collection_name
        self.__is_loaded = False

    async def load(self):
        logging.debug("load()")
        if self.__is_loaded:
            logging.warning("Already loaded")
            return

        if self.qdrant_config.qdrant_url is not None:
            self.qdrant_cli = QdrantClient(url=self.qdrant_config.qdrant_url)
        elif self.qdrant_config.qdrant_db_path is not None:
            self.qdrant_cli = QdrantClient(path=self.qdrant_config.qdrant_db_path)
        else:
            raise AssertionError("qdrant_uri or qdrant_db_path not set")

        self.__ensure_quadrant_collection_created()
        self.__is_loaded = True

    async def create_document(
            self,
            data: str,
            source_link: str | None = None,
            metadata: dict = {},
    ) -> Document:
        if not self.__is_loaded:
            raise AssertionError("Calling add_document() for not loaded instance!")

        metadata[SOURCE_LINK_KEY] = source_link
        ids = self.qdrant_cli.add(
            collection_name=self.collection_name,
            documents=[data],
            metadata=[metadata],
        )
        return Document(
            id=ids[0],
            data=data,
            source_link=source_link,
            metadata=metadata,
        )

    async def delete_document(self, doc_id: DocId):
        self.qdrant_cli.delete(collection_name=self.collection_name, points_selector=[doc_id])

    async def get_all_docs(self) -> Iterable[Document]:
        return QdrantDocsIterable(qdrant_cli=self.qdrant_cli, collection_name=self.collection_name)

    async def get_relevant_docs(self, query: str) -> List[Document]:
        response_docs: List[QueryResponse] = self.qdrant_cli.query(collection_name=self.collection_name,
                                                                   query_text=query,
                                                                   limit=self.relevant_docs_limit)
        return [DocumentMapper.from_qdrant_response(d) for d in response_docs]

    async def close(self):
        if not self.__is_loaded:
            return
        try:
            self.qdrant_cli.close()
            self.__is_loaded = False
        except Exception as e:
            logging.error(e)

    async def clear(self):
        if not self.__is_loaded:
            raise AssertionError("Calling clear() for not loaded instance!")
        if self.qdrant_cli.collection_exists(collection_name=self.collection_name):
            self.qdrant_cli.delete_collection(collection_name=self.collection_name)

    def __ensure_quadrant_collection_created(self):
        if not self.qdrant_cli.collection_exists(collection_name=self.collection_name):
            self.qdrant_cli.create_collection(
                collection_name=self.collection_name,
                vectors_config=self.qdrant_cli.get_fastembed_vector_params(),
            )
