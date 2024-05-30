from discord import Client, Intents, Message
from typing import Callable, Awaitable


_SCRIPTLY_PREFIX = "[Scriptly] "
_SCRIPTLY_PREFIX_LENGTH = len(_SCRIPTLY_PREFIX)


class Bot(Client):
    type Callback = Callable[[Bot, Message, str, list[str]], Awaitable[None]]

    _phrases: list[str]
    _callback: Callback

    def __init__(self, phrases: list[str], callback: Callback) -> None:
        super().__init__(
            intents=Intents.all(),
        )
        self._phrases = phrases
        self._callback = callback

    async def on_message(self, message: Message):
        if not message.author.bot or not message.author.name.startswith(_SCRIPTLY_PREFIX):
            return
        
        user_name = message.author.name[_SCRIPTLY_PREFIX_LENGTH:]

        content = message.content.lower()
        phrases: list[str] = []
        for phrase in self._phrases:
            if phrase in content:
                phrases.append(phrase)
        
        if phrases:
            await self._callback(self, message, user_name, phrases)
