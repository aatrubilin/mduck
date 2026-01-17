import random
from typing import cast

import ollama


class OllamaRepository:
    """A repository for interacting with the Ollama API."""

    def __init__(
        self,
        host: str,
        model: str,
        temperature: float,
        system_prompts: list[str],
    ) -> None:
        """
        Initialize the OllamaRepository.

        Args:
        ----
            host: The Ollama API host.
            model: The model to use for generating responses.
            temperature: The temperature to use for generating responses.
            system_prompts: A list of system prompts to use.

        """
        self._client = ollama.Client(host=host)
        self._model = model
        self._temperature = temperature
        self._system_prompts = system_prompts

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response from the Ollama API.

        Args:
        ----
            prompt: The user prompt.

        Returns:
        -------
            The response from the Ollama API.

        """
        system_prompt = random.choice(self._system_prompts)
        response = self._client.chat(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            options=ollama.Options(temperature=self._temperature),
        )
        return cast(str, response["message"]["content"])
