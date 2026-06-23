from abc import ABC
from abc import abstractmethod

import requests


class LLMBackend(ABC):

    @abstractmethod
    def generate(
        self,
        question,
        context_blocks
    ):
        pass


class OllamaBackend(
    LLMBackend
):

    def __init__(
        self,
        model_name
    ):
        self.model_name = model_name

    def generate(
        self,
        question,
        context_blocks
    ):

        context = "\n\n".join(
            context_blocks
        )

        prompt = f"""
You are GitGPT.

Answer ONLY from repository context.

QUESTION:
{question}

CONTEXT:
{context}

ANSWER:
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        response.raise_for_status()

        return response.json()[
            "response"
        ]


class OpenAIBackend(
    LLMBackend
):

    def __init__(
        self,
        model_name,
        api_key
    ):
        self.model_name = model_name
        self.api_key = api_key

    def generate(
        self,
        question,
        context_blocks
    ):

        try:
            from openai import OpenAI

            client = OpenAI(
                api_key=self.api_key
            )

            context = "\n\n".join(
                context_blocks
            )

            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content":
                        "Answer only from repository context."
                    },
                    {
                        "role": "user",
                        "content":
                        f"Question: {question}\n\nContext:\n{context}"
                    }
                ]
            )

            return response.choices[
                0
            ].message.content

        except Exception as e:

            raise RuntimeError(
                f"OpenAI error: {e}"
            )


class AnthropicBackend(
    LLMBackend
):

    def __init__(
        self,
        model_name,
        api_key
    ):
        self.model_name = model_name
        self.api_key = api_key

    def generate(
        self,
        question,
        context_blocks
    ):

        try:

            import anthropic

            client = anthropic.Anthropic(
                api_key=self.api_key
            )

            context = "\n\n".join(
                context_blocks
            )

            response = client.messages.create(
                model=self.model_name,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content":
                        f"""
Question:
{question}

Repository Context:
{context}
"""
                    }
                ]
            )

            return response.content[
                0
            ].text

        except Exception as e:

            raise RuntimeError(
                f"Anthropic error: {e}"
            )


def get_backend(
    provider,
    model,
    api_key=None
):

    provider = provider.lower()

    if provider == "ollama":

        return OllamaBackend(
            model
        )

    if provider == "openai":

        return OpenAIBackend(
            model,
            api_key
        )

    if provider == "anthropic":

        return AnthropicBackend(
            model,
            api_key
        )

    raise ValueError(
        f"Unknown provider: {provider}"
    )