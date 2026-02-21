from openai import OpenAI


class OpenAIClient:
    def __init__(self, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def explain_failure(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            temperature=0.2,
        )
        return response.output_text.strip()