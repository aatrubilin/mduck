"""Router for new chat members."""

from aiogram import Router, types
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from dependency_injector.wiring import Provide, inject

from mduck.containers.application import ApplicationContainer
from mduck.services.mduck import MDuckService

router = Router(name="chat_member")


@router.my_chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
@inject
async def new_chat_member_handler(
    event: types.ChatMemberUpdated,
    mduck: MDuckService = Provide[ApplicationContainer.mduck],
) -> None:
    """Handle new chat members."""
    await mduck.handle_new_chat_member(event)
