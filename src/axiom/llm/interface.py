from abc import ABC, abstractmethod

from axiom.llm.schemas import LLMRequest, LLMResponse


class LLMInterface(ABC):

    @abstractmethod
    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        ...