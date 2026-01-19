from http import HTTPStatus
from typing import Annotated, Any

import aiogram
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Header, HTTPException

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("/{path}")
@inject
async def webhook(
    path: str,
    update: dict[str, Any],
    dp: Annotated[aiogram.Dispatcher, Depends(Provide["dispatcher"])],
    bot: Annotated[aiogram.Bot, Depends(Provide["gateways.bot"])],
    key: Annotated[str, Depends(Provide["config.tg.webhook.key"])],
    secret: Annotated[str, Depends(Provide["config.tg.webhook.secret"])],
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None,
) -> dict[str, str]:
    """Return a healthcheck."""
    if path != key:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    if x_telegram_bot_api_secret_token != secret:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    await dp.feed_webhook_update(bot, update)
    return {"status": "ok", "path": str(key), "secret": str(secret)}
