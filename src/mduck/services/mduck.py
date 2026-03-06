import asyncio
import logging
import random

from aiogram import Bot, types
from aiogram.enums import ChatAction, ChatType, ParseMode
from redis.asyncio import Redis

from mduck.repositories.ollama import OllamaRepository
from mduck.schemas.queue import MessagePayload, QueueMessage

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
        'File that under *"who asked?"*',
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
        'I’ll put that in my *"meh"* folder.',
        "You done, or is there more pain?",
        "That’s a no from me, duckling.❌",
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
        'That? A masterpiece of *"meh"*.',
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

    STICKER_PACKS = [
        {
            "1_quack_you": "CAACAgIAAxkBAAPRaXuwcTrfizLyamUwc4Vd4B5sHsAAAh2VAAKh7NlLexqb66bnMPc4BA",  # noqa: E501
            "2_facepalm": "CAACAgIAAxkBAAPXaXuxPwx10wKX0SS-HcEs2rWEJTcAAvaUAAJQ3dlL95OViFZHxwY4BA",  # noqa: E501
            "3_hello": "CAACAgIAAxkBAAPZaXuxVR1SkwZbeqYQZmFIPzQe-OYAAh6cAAKn1OBLCoJ3OTCgAAEROAQ",  # noqa: E501
            "4_duck_off": "CAACAgIAAxkBAAPbaXuxZrFuK4gIgG_JGMQU0yVCOYwAAmWTAAJ1r-FLu67QV4xDNG04BA",  # noqa: E501
            "5_get_lost": "CAACAgIAAxkBAAPdaXuxcW0anUzG9EWVWGg1ORNhgncAApCVAAIaFuBLZx4TxJrh7_g4BA",  # noqa: E501
            "6_i_dont_give_a_quack": "CAACAgIAAxkBAAPfaXuxfEgc4si8l7UJymXdgeHW5DIAAjCNAAJIROBLcoRw4CzIS3k4BA",  # noqa: E501
            "7_krak_if_you_dare": "CAACAgIAAxkBAAPfaXuxfEgc4si8l7UJymXdgeHW5DIAAjCNAAJIROBLcoRw4CzIS3k4BA",  # noqa: E501
            "8_shut_it": "CAACAgIAAxkBAAPhaXuxnbwEA8vC50aNBk-xuSDPWA0AAlGgAAJqx9lLiEiTaTsF7m44BA",  # noqa: E501
            "9_youve_quacked_your_last": "CAACAgIAAxkBAAPjaXuxqKXaSPDn_oqR5qJrDLr3ThUAAsaOAAL7xeFLJzkAAcSOrNveOAQ",  # noqa: E501
            "10_quack_you_v2": "CAACAgIAAxkBAAPlaXuxtUxHwmvpKx_26fxI8j0h-5gAAnWRAAJ3rOFLaH-EREb78to4BA",  # noqa: E501
            "11_kiss": "CAACAgIAAxkBAAIBuWmrH6nMmz7tiacJBEogVpMmnLGOAALxjgAC0hxRSZSwsnWmF4ayOgQ",  # noqa: E501
        }
    ]

    WELCOME_STICKERS = [
        STICKER_PACKS[0]["1_quack_you"],
        STICKER_PACKS[0]["2_facepalm"],
        STICKER_PACKS[0]["3_hello"],
        STICKER_PACKS[0]["9_youve_quacked_your_last"],
        STICKER_PACKS[0]["10_quack_you_v2"],
        STICKER_PACKS[0]["7_krak_if_you_dare"],
        STICKER_PACKS[0]["11_kiss"],
    ]

    def __init__(
        self,
        bot: Bot,
        ollama_repository: OllamaRepository,
        redis: Redis,
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
        self._redis = redis
        self._response_probability = {
            ChatType.PRIVATE.value: response_probability_private,
            ChatType.GROUP.value: response_probability_group,
            ChatType.SUPERGROUP.value: response_probability_supergroup,
        }
        self._max_queue_size = max_queue_size
        self._message_queue_key = "mduck:message_queue"
        self._chats_in_queue_key = "mduck:chats_in_queue"
        logger.info(
            "MDuckService initialized with probability: %s, max_queue_size: %s",
            self._response_probability,
            self._max_queue_size,
        )

    async def _send_typing_periodically(
        self,
        chat_id: int,
        stop_event: asyncio.Event,
        interval: int = 30,
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

        sticker_id = random.choice(self.WELCOME_STICKERS)
        await event.answer_sticker(sticker_id)
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

    async def send_random_sticker(self, message: types.Message) -> None:
        """Send a random sticker."""
        random_pack = random.choice(self.STICKER_PACKS)
        random_sticker_key, random_sticker = random.choice(list(random_pack.items()))
        logger.info(f"Sending random sticker {random_sticker_key}")
        random_sticker = random_pack[random_sticker_key]
        await message.answer_sticker(random_sticker)

    async def handle_incoming_message(self, message: types.Message) -> None:
        """
        Handle an incoming message, deciding whether to queue it for a response.

        The message is queued if the chat does not already have a message in the
        queue and if the probability check passes.

        :param message: The incoming aiogram Message object.
        """
        is_in_queue = await self._redis.sismember(  # type: ignore[misc]
            self._chats_in_queue_key, str(message.chat.id)
        )
        if is_in_queue:
            logger.debug(
                "Chat %s already has a message in queue, skipping.", message.chat.id
            )
            return

        if not message.text:
            return
        bot_info: types.User = await self._bot.me()
        if f"@{bot_info.username}" in message.text or (
            message.reply_to_message
            and message.reply_to_message.from_user
            and message.reply_to_message.from_user.id == self._bot.id
        ):
            response_probability = 1.0
        else:
            response_probability = self._response_probability.get(
                message.chat.type, 0.0
            )

        probability = random.random()
        if probability < response_probability:
            queue_size = await self._redis.scard(self._chats_in_queue_key)  # type: ignore[misc]
            if queue_size >= self._max_queue_size:
                logger.warning(
                    "Message queue is full (%s messages), "
                    "skipping message from chat %s.",
                    self._max_queue_size,
                    message.chat.id,
                )
                await self.send_random_sticker(message)
                return
            else:
                if random.choice([True, False]):
                    await self.send_random_sticker(message)
                    return

            payload = MessagePayload(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text=message.text,
                chat_type=message.chat.type,
            )
            queue_message = QueueMessage(message=payload)

            await self._redis.lpush(  # type: ignore[misc]
                self._message_queue_key, queue_message.model_dump_json()
            )
            await self._redis.sadd(self._chats_in_queue_key, str(message.chat.id))  # type: ignore[misc]
            logger.info("Message from chat %s queued for processing.", message.chat.id)
        else:
            logger.debug(
                "Message from chat %s skipped due to probability: %s > %s",
                message.chat.id,
                probability,
                response_probability,
            )
            if message.chat.type == ChatType.PRIVATE:
                if random.choice([True, False]):
                    await message.answer(
                        random.choice(self.PRIVATE_MESSAGES),
                        parse_mode=ParseMode.MARKDOWN,
                    )
                else:
                    await self.send_random_sticker(message)

    async def process_message_from_queue(self) -> None:
        """
        Wait for a message from the queue, process it, and send a reply.

        This method is intended to be run as a continuous background task.
        """
        try:
            _key, raw_message = await self._redis.brpop(  # type: ignore[misc]
                [self._message_queue_key]
            )
            queue_message = QueueMessage.model_validate_json(raw_message)

            queue_message.context.set_contextvars()

            await self._process_message(queue_message.message)
        except Exception as e:
            logger.error("Error processing message from queue: %s", e, exc_info=True)

    async def _process_message(self, message: MessagePayload) -> None:
        chat_id = message.chat_id
        logger.info("Processing message from chat %s from queue.", chat_id)

        event = asyncio.Event()
        try:
            if message.text is None:
                raise RuntimeError("Empty message text")

            # Send "typing" action in background
            task = asyncio.create_task(self._send_typing_periodically(chat_id, event))

            prompt = message.text

            if prompt.startswith("@"):
                prompt = prompt.split(" ", 1)[1]

            if prompt:
                template, response = await self._ollama_repository.generate_response(
                    prompt
                )

                if response.message and response.message.content:
                    text = response.message.content.strip()
                else:
                    raise RuntimeError("Missed contente response...")
                if random.random() <= 0.2:
                    logger.debug("Add 🦆🦆🦆")
                    text += "🦆"

                eval_count = response.eval_count or 0
                eval_duration = response.eval_duration or 1

                tps = eval_count / eval_duration * 1e9
                duration = (response.total_duration or 0) / 1e9

                meta = (
                    f"Duration: {duration:.2f}sec\n"
                    f"Tokens: {response.prompt_eval_count} -> {response.eval_count}\n"
                    f"Speed: {tps:.1f}tps\n"
                    f"Prompt: {template}"
                )

                if message.chat_type == ChatType.PRIVATE:
                    text += f"\n\n```metadata\n{meta}```"

                # Send the response
                await self._bot.send_message(
                    chat_id=chat_id,
                    text=text,
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
                await self._bot.send_message(
                    chat_id=chat_id,
                    text="Quack! *ERROR* 0xQUACK\n"
                    "Duck OS has temporarily lost control of the feathers.\n"
                    "Suggested fixes:\n"
                    "  • flap wings aggressively\n"
                    "  • quack exactly three times\n"
                    "  • wait until I paddle back to shore\n"
                    "Quaaaack… restarting in wet mode ♡",
                    reply_to_message_id=message.message_id,
                    parse_mode=ParseMode.MARKDOWN,
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
            await self._redis.srem(self._chats_in_queue_key, str(chat_id))  # type: ignore[misc]
            logger.debug("Chat %s removed from queued messages set.", chat_id)
