"""Tests for the whoami router."""

from fastapi.testclient import TestClient


def test_whoami(client: TestClient) -> None:
    """Test the /whoami endpoint."""
    # Arrange
    custom_headers = {"X-Test-Header": "TestValue"}

    # Act
    response = client.get("/whoami", headers=custom_headers)

    # Assert
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["client.host"] == "testclient"
    assert response_json["x-test-header"] == "TestValue"
    assert "host" in response_json
    assert "user-agent" in response_json
