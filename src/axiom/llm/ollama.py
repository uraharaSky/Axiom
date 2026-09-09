import requests
from axiom.llm.schemas import LLMRequest, LLMResponse
from axiom.llm.interface import LLMInterface


class OllamaClient:
    def __init__(
            self,
            host: str = "http://localhost:11434",
            model: str = "llama3:latest",
    ):
        self.host = host
        self.model = model

    def generate(self, request: LLMRequest ) -> LLMResponse:
        model = request.model or self.model

        response = requests.post(
            f"{self.host}/api/generate",
            json = {
                "model": model,
                "prompt": request.prompt,
                "stream": False,
            },
        )

        response.raise_for_status()

        data = response.json()

        return LLMResponse(
            content = data["response"],
            model = data["model"],
        )