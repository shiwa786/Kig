import contextlib
import os
import traceback
import typing
from datetime import datetime

import pyrogram

try:
    OWNER_ID = int(os.environ.get("OWNER_ID"))
except ValueError:
    raise Exception("Your OWNER_ID env variable is not a valid integer.")

LOGGER_ID = os.environ.get("LOGGER_ID", None)

log_chat = OWNER_ID if LOGGER_ID is None else LOGGER_ID


async def handle_error(
    error, m: typing.Union[pyrogram.types.Message, pyrogram.types.CallbackQuery]
):
    day = datetime.now()
    tgl_now = datetime.now()
    cap_day = f"{day.strftime('%A')}, {tgl_now.strftime('%d %B %Y %H:%M:%S')}"

    with open(
        f"crash_{tgl_now.strftime('%d %B %Y')}.txt", "w+", encoding="utf-8"
    ) as log:
        log.write(traceback.format_exc())
        log.close()
    if isinstance(m, pyrogram.types.Message):
        with contextlib.suppress(Exception):
            await m.reply_text(
                "ᴀɴ ɪɴᴛᴇʀɴᴀʟ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ᴄᴏᴍᴍᴀɴᴅ.\nsᴏʀʀʏ ғᴏʀ ɪɴᴄᴏɴᴠᴇɴɪᴇɴᴄᴇ"
            )
            await m._client.send_document(
                log_chat,
                f"crash_{tgl_now.strftime('%d %B %Y')}.txt",
                caption=f"ᴄʀᴀsʜ ʀᴇᴘᴏʀᴛ ᴏғ ᴛʜɪs ʙᴏᴛ\n{cap_day}",
            )
    if isinstance(m, pyrogram.types.CallbackQuery):
        with contextlib.suppress(Exception):
            await m.message.delete()
            await m.message.reply_text(
                "ᴀɴ ɪɴᴛᴇʀɴᴀʟ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ᴄᴏᴍᴍᴀɴᴅ.\nsᴏʀʀʏ ғᴏʀ ɪɴᴄᴏɴᴠᴇɴɪᴇɴᴄᴇ"
            )
            await m.message._client.send_document(
                log_chat,
                f"crash_{tgl_now.strftime('%d %B %Y')}.txt",
                caption=f"ᴄʀᴀsʜ ʀᴇᴘᴏʀᴛ ᴏғ ᴛʜɪs ʙᴏᴛ\n{cap_day}",
            )
    os.remove(f"crash_{tgl_now.strftime('%d %B %Y')}.txt")
    return True
