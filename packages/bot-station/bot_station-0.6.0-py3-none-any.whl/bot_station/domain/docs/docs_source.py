from abc import ABC, abstractmethod
from typing import List

from bot_station.domain.docs.model.document import Document


class DocsSource(ABC):

    @abstractmethod
    async def get_relevant_docs(self, query: str) -> List[Document]:
        pass
