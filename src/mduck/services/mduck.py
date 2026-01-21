import asyncio
import contextvars
import logging
import random

from aiogram import Bot, types
from aiogram.enums import ChatAction, ChatType, ParseMode

from mduck.repositories.ollama import OllamaRepository

logger = logging.getLogger(__name__)


class MDuckService:
    """
    A service for handling incoming messages with a certain probability.

    Placing them in a queue, and processing them later.
    """

    PRIVATE_MESSAGES = [
        "Oh, thrilling. 🙄",
        "**Fascinating. Truly.**",
        "Be still, my feathers. 🦆",
        "Riveting. Next.",
        "_Quackin’ joy._",
        "Hold my pond. 🐾",
        "Yawn. Try harder.",
        "Groundbreaking. Not. 💩",
        "Wow. A revelation. 🚬",
        "I care. Deeply. **Not.**",
        "Neat. Tell someone who cares.",
        "Oh, the drama. 🎭",
        "File that under *“who asked?”*",
        "Gasp. Not really.",
        "Earth-shattering. Like a wet sock. 🧦",
        "Color me uninterested.",
        "_My enthusiasm is drowning._",
        "Can’t wait to ignore that.",
        "Did I ask? Didn’t think so. 🤷",
        "**Quack off.**",
        "Stunning. Like beige.",
        "I’ll alert the press. 🗞️",
        "Riveting. Like watching algae grow.",
        "Be still my dead soul. ☠️",
        "Wow. So original. 💤",
        "Another masterpiece. In mediocrity.",
        "I’m on the edge. Of sleep.",
        "Tell it to a brick wall. 🧱",
        "Oh joy. Another word salad. 🥗",
        "That’s one way to waste air.",
        "My tail feathers are trembling. 🪶",
        "I’ll put that in my *“meh”* folder.",
        "You done, or is there more pain?",
        "That’s a no from me, duckling. ❌",
        "I’m riveted. To the exit. 🚪",
        "Quacktastic. In the worst way.",
        "I’d care less, but physics won’t allow it.",
        "That’s a solid nope. 🧊",
        "I live for this nonsense. Not.",
        "You’re still talking? 💤",
        "**Consider me underwhelmed.**",
        "I’ve seen puddles deeper than that. 🌊",
        "Fascinating. Like wet toast.",
        "I’ll pretend to care. Briefly.",
        "That’s going in the trash fire. 🔥",
        "I’m moved. To leave. 🦶",
        "Groundbreaking. Like a stubbed toe.",
        "Stop. My brain is melting. 🧠💧",
        "I’d clap, but sarcasm doesn’t echo. 👏",
        "You win the award. For noise. 🏆",
        "Cool. Like lukewarm soup. 🍲",
        "Oh, look. Another opinion.",
        "Tell me more. So I can forget it.",
        "That’s rich. Like expired milk. 🥴",
        "I’m floored. By boredom.",
        "Alert the ducks. We’ve got nonsense. 🦆🚨",
        "Spectacular. In a trainwreck kind of way. 🚂💥",
        "I’d jump for joy, but I’m allergic.",
        "Wow. A real page-turner. 📖",
        "I’ll add that to my list of regrets. 📝",
        "You’re killing me. With mediocrity.",
        "I felt that. In my indifference.",
        "You should bottle that. As a sedative. 💊",
        "That idea? Straight from the swamp. 🐸",
        "I’d say wow, but I’m not a liar.",
        "My silence is applause. 👏",
        "You’ve outdone yourself. Again. Sadly.",
        "I’m stunned. Into apathy.",
        "That? A masterpiece of *‘meh’*.",
        "I’m crying. From boredom. 😢",
        "Oh no. Anyway. 🙃",
        "You brought words. I brought regret.",
        "That’s a plot twist. Of nothing.",
        "I’d rate that a solid **2 out of nope.**",
        "Bravo. For trying. 👏",
        "My interest just flatlined. 📉",
        "You’re the reason I molt early. 🪶",
        "A+ for effort. F for impact.",
        "That’s a bold choice. To speak.",
        "You’re like static. But louder. 📻",
        "I’m not mad. Just disappointed. 😐",
        "You had me. Then lost me. Instantly.",
        "That’s deep. Like a puddle.",
        "I’ve heard ducks quack smarter things. 🦆",
        "You just wasted a perfectly good breath.",
        "That’s one way to fill the silence.",
        "I’m not ignoring you. I’m surviving.",
        "You’re the background noise of life. 🔇",
        "That thought? Should’ve stayed inside.",
        "You’ve got potential. For silence. 🤐",
        "I’m hanging on every word. *With a noose.* 🪢",
        "That’s not even wrong. Just sad.",
        "I’d argue, but why bother?",
        "You’re not wrong. Just irrelevant.",
        "I’m impressed. At your consistency.",
        "You’ve reached new levels. Of low. 🕳️",
        "That’s the spirit. Of confusion.",
        "You’re a walking shrug. 🤷‍♂️",
        "I’d say something, but you’d miss it.",
        "You’re like déjà vu. But worse.",
        "You just reinvented the wheel. As a square. 🔲",
        "That’s not input. That’s noise.",
        "I’d respond, but I respect my time. ⏳",
        "You done flapping, or should I nap? 😴",
    ]

    def __init__(
        self,
        bot: Bot,
        ollama_repository: OllamaRepository,
        response_probability_private: float = 0.2,
        response_probability_group: float = 0.01,
        response_probability_supergroup: float = 0.001,
        max_queue_size: int = 10,
    ) -> None:
        """
        Initialize the MDuckService.

        :param ollama_repository: The repository for interacting with Ollama.
        :param response_probability: The chance (0.0 to 1.0) of responding to a message.
        :param max_queue_size: The maximum number of messages in the queue.
        """
        self._bot = bot
        self._ollama_repository = ollama_repository
        self._response_probability = {
            ChatType.PRIVATE.value: response_probability_private,
            ChatType.GROUP.value: response_probability_group,
            ChatType.SUPERGROUP.value: response_probability_supergroup,
        }
        self.message_queue: asyncio.Queue[tuple[contextvars.Context, types.Message]] = (
            asyncio.Queue()
        )
        self.chats_with_queued_message: set[int] = set()
        self._max_queue_size = max_queue_size
        logger.info(
            "MDuckService initialized with probability: %s, max_queue_size: %s",
            self._response_probability,
            self._max_queue_size,
        )

    async def _send_typing_periodically(
        self, chat_id: int, stop_event: asyncio.Event, interval: int = 4
    ) -> None:
        """Send 'typing' chat action periodically until stop_event is set."""
        while not stop_event.is_set():
            try:
                logger.info("Sending typing...")
                await self._bot.send_chat_action(
                    chat_id=chat_id, action=ChatAction.TYPING
                )
            except Exception as e:
                logger.warning(
                    "Failed to send typing action to chat %s: %s", chat_id, e
                )
            await asyncio.sleep(interval)

    async def _handle_bot_is_added(self, event: types.ChatMemberUpdated) -> None:
        """Handle bot added."""
        await event.answer("🦆 *MooDuck* entered the chat.", parse_mode="Markdown")
        await event.answer_sticker(
            "CAACAgIAAxkBAAM6aWn2HORULYp5Uiioos8LjHZrAUIAAvYAA1advQr3204hQD6lijgE",
        )
        await self._bot.send_chat_action(
            chat_id=event.chat.id,
            action=ChatAction.TYPING,
        )
        await asyncio.sleep(2)

        await event.answer(
            "Krak. Looks like this group needed more sarcasm.\n\n"
            "I don't help. I judge.\n"
            "I don't fix. I mock.\n\n"
            "Too late to regret now.",
        )

    async def handle_new_chat_member(self, event: types.ChatMemberUpdated) -> None:
        """Handle bot is added to chat."""
        user = event.new_chat_member.user
        if user.id == self._bot.id:
            await self._handle_bot_is_added(event)

    async def handle_incoming_message(self, message: types.Message) -> None:
        """
        Handle an incoming message, deciding whether to queue it for a response.

        The message is queued if the chat does not already have a message in the
        queue and if the probability check passes.

        :param message: The incoming aiogram Message object.
        """
        if message.chat.id in self.chats_with_queued_message:
            logger.debug(
                "Chat %s already has a message in queue, skipping.", message.chat.id
            )
            return

        if not message.text:
            return
        bot_info: types.User = await self._bot.me()
        if f"@{bot_info.username}" in message.text or (
            message.reply_to_message
            and message.reply_to_message.text
            and message.reply_to_message.from_user
            and message.reply_to_message.from_user.id == self._bot.id
        ):
            logger.info("Reply to bot or tag bot")
            response_probability = 1.0
        else:
            response_probability = self._response_probability.get(
                message.chat.type, 0.0
            )

        probability = random.random()
        if probability < response_probability:
            if len(self.chats_with_queued_message) >= self._max_queue_size:
                logger.warning(
                    "Message queue is full (%s messages), "
                    "skipping message from chat %s.",
                    self._max_queue_size,
                    message.chat.id,
                )
                return

            context = contextvars.copy_context()
            self.message_queue.put_nowait((context, message))
            self.chats_with_queued_message.add(message.chat.id)
            logger.info("Message from chat %s queued for processing.", message.chat.id)
        else:
            logger.debug(
                "Message from chat %s skipped due to probability: %s > %s",
                message.chat.id,
                probability,
                response_probability,
            )
            if message.chat.type == ChatType.PRIVATE:
                await message.answer(
                    random.choice(self.PRIVATE_MESSAGES), parse_mode=ParseMode.MARKDOWN
                )

    async def process_message_from_queue(self) -> None:
        """
        Wait for a message from the queue, process it, and send a reply.

        This method is intended to be run as a continuous background task.
        """
        context, message = await self.message_queue.get()
        await context.run(self._process_message, message)

    async def _process_message(self, message: types.Message) -> None:
        chat_id = message.chat.id
        logger.info("Processing message from chat %s from queue.", chat_id)

        event = asyncio.Event()
        try:
            if message.text is None:
                raise RuntimeError("Empty message text")

            # Send "typing" action in background
            context = contextvars.copy_context()
            task = context.run(
                asyncio.create_task,
                self._send_typing_periodically(chat_id, event),
            )

            if message.reply_to_message and message.reply_to_message.text:
                if message.reply_to_message.from_user:
                    msg_from = ", from ({replied_msg.from_user.full_name})"
                else:
                    msg_from = ""
                replied_msg = message.reply_to_message
                prompt = (
                    "The user is now REPLYING to the previous message.\n"
                    f"Previous message{msg_from} "
                    "(the one being replied to): "
                    f"'''{replied_msg.text}'''\n"
                    f"Current user's reply: '''{message.text}'''"
                )
            else:
                prompt = message.text

            if prompt.startswith("@"):
                prompt = prompt.split(" ", 1)[1]

            if prompt:
                # Generate response from Ollama asynchronously
                response_text = await self._ollama_repository.generate_response(prompt)
                # Send the response
                await message.answer(
                    response_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_to_message_id=message.message_id,
                )

            event.set()
            task.cancel()
            logger.info("Replied to message in chat %s.", chat_id)
        except Exception as e:
            logger.error(
                "Error processing message in chat %s: %s", chat_id, e, exc_info=True
            )
            try:
                await message.answer(
                    "Quack! *ERROR* 0xQUACK\n"
                    "Duck OS has temporarily lost control of the feathers.\n"
                    "Suggested fixes:\n"
                    "  • flap wings aggressively\n"
                    "  • quack exactly three times\n"
                    "  • wait until I paddle back to shore\n"
                    "Quaaaack… restarting in wet mode ♡",
                    reply_to_message_id=message.message_id,
                )
            except Exception as e2:
                logger.error(
                    "Failed to send error message to chat %s: %s",
                    chat_id,
                    e2,
                    exc_info=True,
                )
        finally:
            event.set()
            self.chats_with_queued_message.remove(chat_id)
            self.message_queue.task_done()
            logger.debug("Chat %s removed from queued messages set.", chat_id)
