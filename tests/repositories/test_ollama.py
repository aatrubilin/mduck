from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mduck.repositories.ollama import OllamaRepository


@pytest.mark.asyncio
@patch("ollama.AsyncClient")
@patch("builtins.open")
@patch("json.load")
async def test_generate_response(
    mock_json_load: MagicMock,
    mock_open: MagicMock,
    mock_client_constructor: MagicMock,
) -> None:
    """Test generate_response calls the ollama client correctly."""
    # Arrange
    host = "http://test-host:11434"
    model = "test-model"
    temperature = 0.5
    system_prompts_path = "/tmp/system_prompts.json"
    system_prompts_content = ["You are a test assistant."]
    prompt = "This is a test prompt."
    expected_response = "This is a test response."

    mock_json_load.return_value = system_prompts_content
    mock_open.return_value.__enter__.return_value = MagicMock()  # Mock the file object

    mock_client_instance = AsyncMock()
    mock_response = MagicMock()
    mock_response.message.content = expected_response
    mock_client_instance.chat.return_value = mock_response
    mock_client_constructor.return_value = mock_client_instance

    repository = OllamaRepository(
        host=host,
        model=model,
        temperature=temperature,
        system_prompts_path=system_prompts_path,
    )

    # Act
    response = await repository.generate_response(prompt)

    # Assert
    mock_open.assert_called_once_with(system_prompts_path, "r")
    mock_json_load.assert_called_once()
    mock_client_constructor.assert_called_once_with(host=host)
    mock_client_instance.chat.assert_called_once()
    _, kwargs = mock_client_instance.chat.call_args
    assert kwargs["model"] == model
    assert kwargs["messages"] == [
        {"role": "system", "content": system_prompts_content[0]},
        {"role": "user", "content": prompt},
    ]
    assert kwargs["options"]["temperature"] == temperature
    assert response == expected_response


@pytest.mark.asyncio
@patch("ollama.AsyncClient")
@patch("builtins.open")
@patch("json.load")
async def test_generate_response_raises_on_empty_content(
    mock_json_load: MagicMock,
    mock_open: MagicMock,
    mock_client_constructor: MagicMock,
) -> None:
    """Test generate_response raises RuntimeError if content is None."""
    # Arrange
    host = "http://test-host:11434"
    model = "test-model"
    temperature = 0.5
    system_prompts_path = "/tmp/system_prompts.json"
    system_prompts_content = ["You are a test assistant."]
    prompt = "This is a test prompt."

    mock_json_load.return_value = system_prompts_content
    mock_open.return_value.__enter__.return_value = MagicMock()  # Mock the file object

    mock_client_instance = AsyncMock()
    mock_response = MagicMock()
    mock_response.message.content = None  # Simulate None content
    mock_client_instance.chat.return_value = mock_response
    mock_client_constructor.return_value = mock_client_instance

    repository = OllamaRepository(
        host=host,
        model=model,
        temperature=temperature,
        system_prompts_path=system_prompts_path,
    )

    # Act & Assert
    mock_open.assert_called_once_with(system_prompts_path, "r")
    mock_json_load.assert_called_once()
    with pytest.raises(RuntimeError, match="Empty response from ollama"):
        await repository.generate_response(prompt)
