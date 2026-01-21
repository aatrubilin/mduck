import json
import logging
import random

import ollama

logger = logging.getLogger(__name__)


class OllamaRepository:
    """A repository for interacting with the Ollama API."""

    def __init__(
        self,
        host: str,
        model: str,
        temperature: float,
        system_prompts_path: str,
    ) -> None:
        """
        Initialize the OllamaRepository.

        Args:
        ----
            host: The Ollama API host.
            model: The model to use for generating responses.
            temperature: The temperature to use for generating responses.
            system_prompts_path: A path to list of system prompts.

        """
        self._client = ollama.AsyncClient(host=host)
        self._model = model
        self._temperature = temperature
        with open(system_prompts_path, "r") as fp:
            self._system_prompts = json.load(fp)
        logger.info(
            "Ollama repo inited with host: %s, %s sys prompts",
            host,
            len(self._system_prompts),
        )

    async def generate_response(self, prompt: str) -> str:
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
        logger.info("System prompt: %s", system_prompt)
        logger.info("User prompt: %s", system_prompt)
        response = await self._client.chat(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            options=ollama.Options(temperature=self._temperature),
        )
        if response.message.content is None:
            raise RuntimeError("Empty response from ollama")
        return response.message.content
