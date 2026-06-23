from abc import ABC, abstractmethod

import requests


class LLMBackend(ABC):

    @abstractmethod
    def generate(
        self,
        question,
        context_blocks
    ):
        pass


class OllamaBackend(LLMBackend):

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
            context_blocks[:3]
        )

        prompt = f"""
You are GitGPT.

You are a repository analysis assistant.

RULES:
- Use ONLY the repository context.
- Do NOT invent information.
- Mention files, classes and methods when possible.
- If the answer is not found in the repository, say:
  "I could not find enough information in the repository."

QUESTION:
{question}

REPOSITORY CONTEXT:
{context}

FINAL ANSWER:
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0,
                    "top_p": 1
                }
            },
            timeout=600
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            ""
        ).strip()


class OpenAIBackend(LLMBackend):

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
                context_blocks[:3]
            )

            response = (
                client.chat.completions.create(
                    model=self.model_name,
                    temperature=0,
                    messages=[
                        {
                            "role": "system",
                            "content": """
You are GitGPT.

Answer ONLY using repository context.

Never use outside knowledge.
Never invent APIs, files, classes or behavior.
"""
                        },
                        {
                            "role": "user",
                            "content": f"""
QUESTION:
{question}

REPOSITORY CONTEXT:
{context}

FINAL ANSWER:
"""
                        }
                    ]
                )
            )

            return (
                response
                .choices[0]
                .message.content
                .strip()
            )

        except Exception as e:

            raise RuntimeError(
                f"OpenAI error: {e}"
            )


class AnthropicBackend(LLMBackend):

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
                context_blocks[:3]
            )

            response = client.messages.create(
                model=self.model_name,
                max_tokens=1000,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": f"""
You are GitGPT.

Answer ONLY using repository context.

QUESTION:
{question}

REPOSITORY CONTEXT:
{context}

If the answer is missing, say:
"I could not find enough information in the repository."

FINAL ANSWER:
"""
                    }
                ]
            )

            return (
                response
                .content[0]
                .text
                .strip()
            )

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

        if not api_key:

            raise ValueError(
                "OpenAI API key missing"
            )

        return OpenAIBackend(
            model,
            api_key
        )

    if provider == "anthropic":

        if not api_key:

            raise ValueError(
                "Anthropic API key missing"
            )

        return AnthropicBackend(
            model,
            api_key
        )

    raise ValueError(
        f"Unsupported provider: {provider}"
    )