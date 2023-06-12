from platform import python_version as py
from pyrogram import __version__ as pyro
from pyrogram import idle
from uvloop import install

from mercu import *
from mercu.config import *

from importlib import import_module
from platform import python_version

from mercu.modules import loadModule
from pyrogram import __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli



MSG_ON = """
**Haidar Premium Actived ✅**
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
◉ **Versi** : `{}`
◉ **Phython** : `{}`
◉ **Pyrogram** : `{}`
**Ketik** `{}alive` **untuk Mengecheck Bot**
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
"""

mongo = MongoCli(MONGO_URL)
db = mongo.premium
ubotdb = db.ubot
accesdb = db.acces
usersdb = db.users
logdb = db.gruplog
blchatdb = db.blchat
vardb = db.variable
sudoersdb = db.sudoers


async def get_botlog(user_id: int):
    user_data = await logdb.users.find_one({"user_id": user_id})
    botlog_chat_id = user_data.get("bot_log_group_id") if user_data else None
    return botlog_chat_id


async def main():
    await app.start()
    LOGGER("Startup").info("Memulai Haidar-Pyro Premium..")
    for bot in botlist:
        try:
            await bot.start()
            ex = bot.me
            user = ex.id
            botlog = await get_botlog(user)
            LOGGER("✓").info(f"Started as {ex.first_name} | {ex.id} ")
            try:
                await bot.send_message(botlog, MSG_ON.format(nan, py(), pyro, nay, cmd))
            except BaseException as a:
                LOGGER("Info").warning(f"{a}")

            ids.append(ex.id)
            LOGGER("Info").info("Startup Completed")

        except Exception as e:
            LOGGER("X").info(f"{e}")
    await loadprem()
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    install()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        LOGGER("Logger").info("Stopping Bot! GoodBye")


async def loadprem():
    modules = loadModule()
    for mod in modules:
        imported_module = import_module(f"naya.modules.{mod}")
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                CMD_HELP[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module


async def load_all():
    modules = loadModule()
    for mod in modules:
        imported_module = import_module(f"naya.modules.{mod}")
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                CMD_HELP[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module
    print(f"[🤖 @{app.me.username} 🤖] [🔥 BERHASIL DIAKTIFKAN! 🔥]")
    await app.send_message(
        LOGS,
        f"""
<b>🔥 {app.me.mention} Berhasil Diaktifkan</b>
<b>📘 Python: {python_version()}</b>
<b>📙 Pyrogram: {__version__}</b>
<b>👮‍♂ User: {len(bots._bots)}</b>
""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🗑 TUTUP 🗑", callback_data="0_cls")]],
        ),
    )
