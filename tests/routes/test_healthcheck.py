from fastapi.testclient import TestClient


def test_healthcheck(client: TestClient) -> None:
    """
    Test healthcheck endpoint.

    GIVEN
    WHEN healthcheck endpoint is called
    THEN it should return 200 and status ok
    """
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
