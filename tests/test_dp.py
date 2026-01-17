from aiogram import Dispatcher
from mduck.dp import init_dispatcher
from mduck.handlers import commands, message, new_chat_member


def test_init_dispatcher() -> None:
    """Test the init_dispatcher function."""
    # Act
    dp = init_dispatcher()

    # Assert
    assert isinstance(dp, Dispatcher)
    assert commands.router in dp.sub_routers
    assert new_chat_member.router in dp.sub_routers
    assert message.router in dp.sub_routers
