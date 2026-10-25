from dataclasses import dataclass


@dataclass
class LLMRequest:
    prompt: str


@dataclass
class LLMResponse:
    content: str