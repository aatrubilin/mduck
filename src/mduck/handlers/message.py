"""Echo router."""

import aiogram
from aiogram import F, types
from dependency_injector.wiring import Provide, inject

from mduck.containers.application import ApplicationContainer
from mduck.services.mduck import MDuckService

router = aiogram.Router(name="message")


@router.message(F.text.len() >= 3, F.text.len() <= 300)
@inject
async def message_handler(
    message: types.Message,
    mduck: MDuckService = Provide[ApplicationContainer.mduck],
) -> None:
    """Message handler."""
    await mduck.handle_incoming_message(message)
