import os
import requests

class MistralAPI:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.base_url = "https://api.mistral.ai/v1"

    def generate(self, prompt: str, model: str = "mistral-large-latest") -> str:
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                }
            )
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"API Error: {e}")
            return ""