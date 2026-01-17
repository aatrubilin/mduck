import asyncio
import logging
import random

from aiogram import Bot, types
from aiogram.enums import ChatAction, ParseMode

from mduck.repositories.ollama import OllamaRepository

logger = logging.getLogger(__name__)


class MDuckService:
    """
    A service for handling incoming messages with a certain probability.

    Placing them in a queue, and processing them later.
    """

    def __init__(
        self,
        bot: Bot,
        ollama_repository: OllamaRepository,
        response_probability: float = 0.3,
    ) -> None:
        """
        Initialize the MDuckService.

        :param ollama_repository: The repository for interacting with Ollama.
        :param response_probability: The chance (0.0 to 1.0) of responding to a message.
        """
        self._bot = bot
        self._ollama_repository = ollama_repository
        self._response_probability = response_probability
        self.message_queue: asyncio.Queue[types.Message] = asyncio.Queue()
        self.chats_with_queued_message: set[int] = set()
        logger.info(
            "MDuckService initialized with probability: %s", self._response_probability
        )

    async def _send_typing_periodically(
        self, chat_id: int, stop_event: asyncio.Event, interval: int = 4
    ) -> None:
        """Send 'typing' chat action periodically until stop_event is set."""
        while not stop_event.is_set():
            try:
                await self._bot.send_chat_action(
                    chat_id=chat_id, action=ChatAction.TYPING
                )
            except Exception as e:
                logger.warning(
                    "Failed to send typing action to chat %s: %s", chat_id, e
                )
            await asyncio.sleep(interval)

    def handle_incoming_message(self, message: types.Message) -> None:
        """
        Handle an incoming message, deciding whether to queue it for a response.

        The message is queued if the chat does not already have a message in the
        queue and if the probability check passes.

        :param message: The incoming aiogram Message object.
        """
        if not message.text:
            return
        if message.chat.id in self.chats_with_queued_message:
            logger.debug(
                "Chat %s already has a message in queue, skipping.", message.chat.id
            )
            return

        if random.random() < self._response_probability:
            self.message_queue.put_nowait(message)
            self.chats_with_queued_message.add(message.chat.id)
            logger.info("Message from chat %s queued for processing.", message.chat.id)
        else:
            logger.debug(
                "Message from chat %s skipped due to probability.", message.chat.id
            )

    async def process_message_from_queue(self) -> None:
        """
        Wait for a message from the queue, process it, and send a reply.

        This method is intended to be run as a continuous background task.
        """
        message = await self.message_queue.get()
        chat_id = message.chat.id
        logger.info("Processing message from chat %s from queue.", chat_id)

        try:
            if message.text is None:
                raise RuntimeError("Empty message text")

            # Send "typing" action in background
            event = asyncio.Event()
            asyncio.create_task(self._send_typing_periodically(chat_id, event))

            # Generate response from Ollama asynchronously
            response_text = await self._ollama_repository.generate_response(
                message.text
            )
            event.set()

            # Send the response
            await message.answer(response_text, parse_mode=ParseMode.MARKDOWN)
            logger.info("Replied to message in chat %s.", chat_id)
        except Exception as e:
            logger.error(
                "Error processing message in chat %s: %s", chat_id, e, exc_info=True
            )
            try:
                await message.answer(
                    "Извините, произошла ошибка при обработке вашего сообщения."
                )
            except Exception as e2:
                logger.error(
                    "Failed to send error message to chat %s: %s",
                    chat_id,
                    e2,
                    exc_info=True,
                )
        finally:
            self.chats_with_queued_message.remove(chat_id)
            self.message_queue.task_done()
            logger.debug("Chat %s removed from queued messages set.", chat_id)
