from unittest.mock import MagicMock, patch

from mduck.repositories.ollama import OllamaRepository


@patch("ollama.Client")
def test_generate_response(mock_client_constructor: MagicMock) -> None:
    """Test generate_response calls the ollama client correctly."""
    # Arrange
    host = "http://test-host:11434"
    model = "test-model"
    temperature = 0.5
    system_prompts = ["You are a test assistant."]
    prompt = "This is a test prompt."
    expected_response = "This is a test response."

    mock_client_instance = MagicMock()
    mock_client_instance.chat.return_value = {"message": {"content": expected_response}}
    mock_client_constructor.return_value = mock_client_instance

    repository = OllamaRepository(
        host=host,
        model=model,
        temperature=temperature,
        system_prompts=system_prompts,
    )

    # Act
    response = repository.generate_response(prompt)

    # Assert
    mock_client_constructor.assert_called_once_with(host=host)
    mock_client_instance.chat.assert_called_once()
    _, kwargs = mock_client_instance.chat.call_args
    assert kwargs["model"] == model
    assert kwargs["messages"] == [
        {"role": "system", "content": system_prompts[0]},
        {"role": "user", "content": prompt},
    ]
    assert kwargs["options"]["temperature"] == temperature
    assert response == expected_response
