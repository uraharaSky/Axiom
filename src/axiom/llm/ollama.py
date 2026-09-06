import requests


class OllamaClient:
    def __init__(
            self,
            host: str = "http://localhost:11434",
            model: str = "llama3:latest",
    ):
        self.host = host
        self.model = model

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]