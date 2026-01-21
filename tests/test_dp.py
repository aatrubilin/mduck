from aiogram import Dispatcher

from mduck.dp import init_dispatcher
from mduck.handlers import chat_member, commands, message


def test_init_dispatcher() -> None:
    """Test the init_dispatcher function."""
    # Arrange
    commands.router._parent_router = None
    chat_member.router._parent_router = None
    message.router._parent_router = None

    # Act
    dp = init_dispatcher()

    # Assert
    assert isinstance(dp, Dispatcher)
    assert commands.router in dp.sub_routers
    assert chat_member.router in dp.sub_routers
    assert message.router in dp.sub_routers
