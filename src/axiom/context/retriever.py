from abc import ABC, abstractmethod

from axiom.context.models import RetrievalUnit

class Retriever(ABC):
    @abstractmethod
    def retrieve(
            self,
            query: str,
            units: list[RetrievalUnit],
            limit: int = 5,
    ) -> list[RetrievalUnit]:

        raise NotImplementedError

class LexicalRetriever(Retriever):

    def retrieve(
            self,
            query: str,
            units: list[RetrievalUnit],
            limit: int = 5,
    ) -> list[RetrievalUnit]:

        query_tokens = set(query.lower().split())

        scored = []

        for unit in units:
            text = f"{unit.name} {unit.kind}".lower()
            unit_tokens = set(text.split())

            score = len(query_tokens & unit_tokens)

            if score > 0:
                scored.append((score, unit))

        scored.sort(
            key = lambda item: item[0],
            reverse = True,
        )

        return [unit for _, unit in scored[:limit]]
