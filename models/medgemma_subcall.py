import requests

class MedGemmaSubcall:
    def __init__(self, model_name="gemma:7b-instruct"):
        self.model_name = model_name

    def generate(self, prompt, max_new_tokens=256, temperature=0.1):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_new_tokens
                }
            }
        )
        return response.json()["response"].strip()