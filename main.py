import asyncio

from dotenv import load_dotenv
from twitchAPI.chat import EventData, ChatMessage, ChatCommand, Chat
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from twitchAPI.type import AuthScope, ChatEvent
from dotenv import load_dotenv
import os

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
CHANNEL = "BTMC"


async def on_ready(ready_event: EventData):
    print('Bot ready')
    await ready_event.chat.join_room(CHANNEL)


async def on_message(msg: ChatMessage):
    print(f"{msg.room.name}: {msg.user.name}: {msg.text}")


async def test_command(cmd: ChatCommand):
    await cmd.reply(f"@{cmd.user.name}: HAIIIIIIIII :3")


async def run():
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    chat = await Chat(twitch)
    chat.set_prefix('?')

    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.register_command('test', test_command)

    chat.start()


asyncio.run(run())
