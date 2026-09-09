from abc import ABC, abstractmethod
from axiom.llm.schemas import LLMRequest, LLMRequest, LLMResponse


class LLMInterface(ABC):
    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a response from an LLM"""
        raise NotImplementedError