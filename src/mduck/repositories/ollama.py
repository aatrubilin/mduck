import logging
import random
from pathlib import Path

import ollama
from ollama import ChatResponse

logger = logging.getLogger(__name__)


class OllamaRepository:
    """A repository for interacting with the Ollama API."""

    def __init__(
        self,
        host: str,
        model: str,
        temperature: float,
        prompts_dir_path: str,
    ) -> None:
        """
        Initialize the OllamaRepository.

        Args:
        ----
            host: The Ollama API host.
            model: The model to use for generating responses.
            temperature: The temperature to use for generating responses.
            prompts_dir_path: A path to a directory with .txt prompt files.

        """
        self._client = ollama.AsyncClient(host=host)
        self._model = model
        self._temperature = temperature
        self._system_prompts: dict[str, str] = self._load_prompts(prompts_dir_path)
        self._system_prompts_keys = list(self._system_prompts.keys())
        logger.info(
            "Ollama repo inited with host: %s, %s sys prompts",
            host,
            len(self._system_prompts),
        )

    def _load_prompts(self, path: str) -> dict[str, str]:
        prompts = {}
        for filepath in Path(path).glob("*.txt"):
            with open(filepath, "r", encoding="utf-8") as fp:
                prompts[filepath.name] = fp.read().strip()
        if not prompts:
            raise ValueError(f"No prompts found in {path}")
        return prompts

    async def generate_response(self, prompt: str) -> ChatResponse:
        """
        Generate a response from the Ollama API.

        Args:
        ----
            prompt: The user prompt.

        Returns:
        -------
            The response from the Ollama API.

        """
        random_key = random.choice(self._system_prompts_keys)
        system_prompt = self._system_prompts[random_key]
        num_predict = random.randint(100, 200) if random.random() < 0.5 else None
        logger.info("System prompt: %s, num_predict=%s", random_key, num_predict)

        response = await self._client.chat(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            options=ollama.Options(
                temperature=self._temperature,
                top_p=0.9,
                num_predict=num_predict,
            ),
        )
        return response
