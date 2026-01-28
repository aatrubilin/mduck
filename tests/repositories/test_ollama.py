"""."""

from pathlib import Path

import pytest

from config.settings import Settings
from mduck.containers.application import ApplicationContainer
from mduck.repositories.ollama import OllamaRepository


@pytest.mark.asyncio
async def test_generate_response(container: ApplicationContainer) -> None:
    """Test generate_response."""
    ollama = container.gateways.ollama()

    template_name, response = await ollama.generate_response("test-prompt")
    assert response.message.content == "test-prompt"


def test_load_prompts_failed(settings: Settings, tmp_path: Path) -> None:
    """Test load prompts failed if not found eny prompt."""
    with pytest.raises(ValueError, match="No prompts found in *"):
        OllamaRepository(
            host=settings.ollama.host,
            model=settings.ollama.model,
            temperature=settings.ollama.temperature,
            prompts_dir_path=str(tmp_path),
        )
