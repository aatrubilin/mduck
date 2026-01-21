from typing import Any

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/whoami")
async def whoami(request: Request) -> dict[str, Any]:
    """Whoami handler."""
    client_host = None
    if request.client:
        client_host = request.client.host
    return {"client.host": client_host, **request.headers}
