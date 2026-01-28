"""Tests for the webhook router."""

from fastapi.testclient import TestClient

from mduck.containers.application import ApplicationContainer


def test_webhook_incorrect_path(client: TestClient) -> None:
    """Test that an incorrect path returns a 404 error."""
    response = client.post("/webhook/wrong_path", json={"update_id": 123})
    assert response.status_code == 404


def test_webhook_incorrect_secret(
    client: TestClient, container: ApplicationContainer
) -> None:
    """Test that an incorrect secret token returns a 401 error."""
    key = container.config.tg.webhook.key()
    response = client.post(
        f"/webhook/{key}",
        headers={"X-Telegram-Bot-Api-Secret-Token": "wrong_secret"},
        json={"update_id": 123},
    )
    assert response.status_code == 401


def test_webhook_success(client: TestClient, container: ApplicationContainer) -> None:
    """Test a successful webhook call."""
    # Arrange
    key = container.config.tg.webhook.key()
    secret = container.config.tg.webhook.secret()
    dispatcher_mock = container.dispatcher()
    update_payload = {"update_id": 123, "message": {"text": "hello"}}

    # Act
    response = client.post(
        f"/webhook/{key}",
        headers={"X-Telegram-Bot-Api-Secret-Token": secret},
        json=update_payload,
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    dispatcher_mock.feed_webhook_update.assert_called_once()
    # Check that the mock was called with the bot and the update payload
    call_args, _ = dispatcher_mock.feed_webhook_update.call_args
    assert call_args[0] is container.gateways.bot()
    assert call_args[1] == update_payload
