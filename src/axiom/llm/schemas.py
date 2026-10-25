from dataclasses import dataclass


@dataclass
class LLMRequest:
    prompt: str
    model: str | None = None


@dataclass
class LLMResponse:
    content: str
    model: str | None = None