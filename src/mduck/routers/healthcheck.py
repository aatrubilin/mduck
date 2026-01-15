from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck")
def healthcheck() -> dict[str, str]:
    """Return a healthcheck."""
    return {"status": "ok"}
