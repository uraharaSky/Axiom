from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMRequest:
    prompt: str
    model: Optional[str] = None

@dataclass
class LLMResponse:
    content: str
    model: str
