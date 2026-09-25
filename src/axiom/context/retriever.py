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

    def _tokenize(self, text: str) -> set[str]:
        return set(text.lower().split())

    def _score(
            self,
            query_tokens: set[str],
            unit_tokens: set[str],
    ) -> int:
        return len(query_tokens & unit_tokens)

    def _rank(
            self,
            scored: list[tuple[int, RetrievalUnit]],
    ) -> list[RetrievalUnit]:

        scored.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        return [unit for _, unit in scored]

    def retrieve(
            self,
            query: str,
            units: list[RetrievalUnit],
            limit: int = 5,
    ) -> list[RetrievalUnit]:

        query_tokens = self._tokenize(query)

        scored = []

        for unit in units:
            unit_tokens = self._tokenize(
                f"{unit.name} {unit.kind}"
            )

            score = self._score(
                query_tokens,
                unit_tokens,
            )

            if score > 0:
                scored.append((score, unit))

        ranked = self._rank(scored)

        return ranked[:limit]