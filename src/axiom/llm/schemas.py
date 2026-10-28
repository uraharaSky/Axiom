from dataclasses import dataclass
from axiom.context.models import RetrievalUnit



@dataclass
class LLMRequest:
    prompt: str
    model: str | None = None


@dataclass
class LLMResponse:
    content: str
    model: str | None = None

