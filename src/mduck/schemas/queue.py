from pydantic import BaseModel, Field

from mduck.log import chat_id_var, update_id_var, user_id_var


class MessagePayload(BaseModel):
    """The essential fields from an aiogram Message object for queueing."""

    chat_id: int
    message_id: int
    text: str | None
    chat_type: str


class QueueContext(BaseModel):
    """Context data to be passed in the queue."""

    update_id: str | None = None
    chat_id: str | None = None
    user_id: str | None = None

    @classmethod
    def from_contextvars(cls) -> "QueueContext":
        """Create a QueueContext instance from the current contextvars."""
        return cls(
            update_id=update_id_var.get(),
            chat_id=chat_id_var.get(),
            user_id=user_id_var.get(),
        )

    def set_contextvars(self) -> None:
        """Set the contextvars from the current instance."""
        if self.update_id:
            update_id_var.set(self.update_id)
        if self.chat_id:
            chat_id_var.set(self.chat_id)
        if self.user_id:
            user_id_var.set(self.user_id)


class QueueMessage(BaseModel):
    """Message data to be passed in the queue."""

    message: MessagePayload
    context: QueueContext = Field(default_factory=QueueContext.from_contextvars)
