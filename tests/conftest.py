from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from mduck.main import create_app


@pytest.fixture()
def client() -> Iterator[TestClient]:
    """Return a test client."""
    app = create_app()
    with TestClient(app) as client:
        yield client
