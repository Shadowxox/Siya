

import asyncio
import importlib
from pyrogram import idle
from pyrogram.types import BotCommand
from pytgcalls.exceptions import NoActiveGroupCall
import config
from ShrutiMusic import LOGGER, app, userbot
from ShrutiMusic.core.call import Nand
from ShrutiMusic.misc import sudo
from ShrutiMusic.plugins import ALL_MODULES
from ShrutiMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

COMMANDS = [
    BotCommand("start", "🚀 ꜱᴛᴀʀᴛ ʙᴏᴛ"),
    BotCommand("help", "❓ ʜᴇʟᴘ ᴍᴇɴᴜ ᴀɴᴅ ᴍᴀɴʏ ᴍᴏʀᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴄᴏᴍᴍᴀɴᴅꜱ"),
    BotCommand("ping", "📡 ᴘɪɴɢ ᴀɴᴅ ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ"),
    BotCommand("play", "🎵 ꜱᴛᴀʀᴛ ꜱᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇQᴜᴇꜱᴛᴇᴅ ᴛʀᴀᴄᴋ"),
    BotCommand("vplay", "📹 ꜱᴛᴀʀᴛ ᴠɪᴅᴇᴏ ꜱᴛʀᴇᴀᴍɪɴɢ"),
    BotCommand("playrtmps", "📺 ᴘʟᴀʏ ʟɪᴠᴇ ᴠɪᴅᴇᴏ"),
    BotCommand("playforce", "⚠️ ꜰᴏʀᴄᴇ ᴘʟᴀʏ ᴀᴜᴅɪᴏ ᴛʀᴀᴄᴋ"),
    BotCommand("vplayforce", "⚠️ ꜰᴏʀᴄᴇ ᴘʟᴀʏ ᴠɪᴅᴇᴏ ᴛʀᴀᴄᴋ"),
    BotCommand("pause", "⏸ ᴘᴀᴜꜱᴇ ᴛʜᴇ ꜱᴛʀᴇᴀᴍ"),
    BotCommand("resume", "▶️ ʀᴇꜱᴜᴍᴇ ᴛʜᴇ ꜱᴛʀᴇᴀᴍ"),
    BotCommand("skip", "⏭ ꜱᴋɪᴘ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴛʀᴀᴄᴋ"),
    BotCommand("end", "🛑 ᴇɴᴅ ᴛʜᴇ ꜱᴛʀᴇᴀᴍ"),
    BotCommand("stop", "🛑 ꜱᴛᴏᴘ ᴛʜᴇ ꜱᴛʀᴇᴀᴍ"),
    BotCommand("queue", "📄 ꜱʜᴏᴡ ᴛʀᴀᴄᴋ Qᴜᴇᴜᴇ"),
    BotCommand("auth", "➕ ᴀᴅᴅ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴀᴜᴛʜ ʟɪꜱᴛ"),
    BotCommand("unauth", "➖ ʀᴇᴍᴏᴠᴇ ᴀ ᴜꜱᴇʀ ꜰʀᴏᴍ ᴀᴜᴛʜ ʟɪꜱᴛ"),
    BotCommand("authusers", "👥 ꜱʜᴏᴡ ʟɪꜱᴛ ᴏꜰ ᴀᴜᴛʜ ᴜꜱᴇʀꜱ"),
    BotCommand("cplay", "📻 ᴄʜᴀɴɴᴇʟ ᴀᴜᴅɪᴏ ᴘʟᴀʏ"),
    BotCommand("cvplay", "📺 ᴄʜᴀɴɴᴇʟ ᴠɪᴅᴇᴏ ᴘʟᴀʏ"),
    BotCommand("cplayforce", "🚨 ᴄʜᴀɴɴᴇʟ ꜰᴏʀᴄᴇ ᴀᴜᴅɪᴏ ᴘʟᴀʏ"),
    BotCommand("cvplayforce", "🚨 ᴄʜᴀɴɴᴇʟ ꜰᴏʀᴄᴇ ᴠɪᴅᴇᴏ ᴘʟᴀʏ"),
    BotCommand("channelplay", "🔗 ᴄᴏɴɴᴇᴄᴛ ɢʀᴏᴜᴘ ᴛᴏ ᴄʜᴀɴɴᴇʟ"),
    BotCommand("loop", "🔁 ᴇɴᴀʙʟᴇ/ᴅɪꜱᴀʙʟᴇ ʟᴏᴏᴘ"),
    BotCommand("stats", "📊 ʙᴏᴛ ꜱᴛᴀᴛꜱ"),
    BotCommand("shuffle", "🔀 ꜱʜᴜꜰꜰʟᴇ ᴛʜᴇ Qᴜᴇᴜᴇ"),
    BotCommand("seek", "⏩ ꜱᴇᴇᴋ ꜰᴏʀᴡᴀʀᴅ"),
    BotCommand("seekback", "⏪ ꜱᴇᴇᴋ ʙᴀᴄᴋᴡᴀʀᴅ"),
    BotCommand("song", "🎶 ᴅᴏᴡɴʟᴏᴀᴅ ꜱᴏɴɢ (ᴍᴘ3/ᴍᴘ4)"),
    BotCommand("speed", "⏩ ᴀᴅᴊᴜꜱᴛ ᴀᴜᴅɪᴏ ꜱᴘᴇᴇᴅ (ɢʀᴏᴜᴘ)"),
    BotCommand("cspeed", "⏩ ᴀᴅᴊᴜꜱᴛ ᴀᴜᴅɪᴏ ꜱᴘᴇᴇᴅ (ᴄʜᴀɴɴᴇʟ)"),
    BotCommand("tagall", "📢 ᴛᴀɢ ᴇᴠᴇʀʏᴏɴᴇ"),
]


async def setup_bot_commands():
    """Setup bot commands during startup"""
    try:
        # Set bot commands
        await app.set_bot_commands(COMMANDS)
        LOGGER("ShrutiMusic").info("Bot commands set successfully!")
        
    except Exception as e:
        LOGGER("ShrutiMusic").error(f"Failed to set bot commands: {str(e)}")

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    await sudo()

    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()
    
    # Setup bot commands during startup
    await setup_bot_commands()

    for all_module in ALL_MODULES:
        importlib.import_module("ShrutiMusic.plugins" + all_module)

    LOGGER("ShrutiMusic.plugins").info("Successfully Imported Modules...")

    await userbot.start()
    await Nand.start()

    try:
        await Nand.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("ShrutiMusic").error(
            "Please turn on the videochat of your log group\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass

    await Nand.decorators()

    LOGGER("ShrutiMusic").info(
        "\x53\x68\x72\x75\x74\x69\x20\x4d\x75\x73\x69\x63\x20\x53\x74\x61\x72\x74\x65\x64\x20\x53\x75\x63\x63\x65\x73\x73\x66\x75\x6c\x6c\x79\x2e\x0a\x0a\x44\x6f\x6e\x27\x74\x20\x66\x6f\x72\x67\x65\x74\x20\x74\x6f\x20\x76\x69\x73\x69\x74\x20\x40\x53\x68\x72\x75\x74\x69\x42\x6f\x74\x73"
    )

    await idle()

    await app.stop()
    await userbot.stop()
    LOGGER("ShrutiMusic").info("Stopping Shruti Music Bot...🥺")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())


