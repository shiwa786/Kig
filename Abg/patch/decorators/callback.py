
import typing
from logging import getLogger

import pyrogram

from pyrogram.methods import Decorators

LOGGER = getLogger(__name__)
def callback(
        self,
        data: typing.Union[str, list],
        self_admin: typing.Union[bool, bool] = False,
        filter: typing.Union[pyrogram.filters.Filter, pyrogram.filters.Filter] = None,
        *args,
        **kwargs,
    ):
        """
        ### `Client.callback`

        - A decorater to Register Callback Quiries in simple way and manage errors in that Function itself, alternative for `@pyrogram.Client.on_callback_query(pyrogram.filters.regex('^data.*'))`
        - Parameters:
        - data (str || list):
            - The callback query to be handled for a function

        - self_admin (bool) **optional**:
            - If True, the command will only executeed if the Bot is Admin in the Chat, By Default False

        - filter (`~pyrogram.filters`) **optional**:
            - Pyrogram Filters, hope you know about this, for Advaced usage. Use `and` for seaperating filters.

        #### Example
        .. code-block:: python
            import pyrogram

            app = pyrogram.Client()

            @app.command("start")
            async def start(client, message):
                await message.reply_text(
                f"Hello {message.from_user.mention}",
                reply_markup=pyrogram.types.InlineKeyboardMarkup([[
                    pyrogram.types.InlineKeyboardButton(
                    "Click Here",
                    "data"
                    )
                ]])
                )

            @app.callback("data")
            async def data(client, CallbackQuery):
            await CallbackQuery.answer("Hello :)", show_alert=True)
        """
        if filter:
            filter = pyrogram.filters.regex(f"^{data}.*") & args["filter"]
        else:
            filter = pyrogram.filters.regex(f"^{data}.*")

        def wrapper(func):
            async def decorator(client, CallbackQuery: pyrogram.types.CallbackQuery):
                if self_admin:
                    me = await client.get_chat_member(
                        CallbackQuery.message.chat.id, (await client.get_me()).id
                    )
                    if me.status not in (
                        pyrogram.enums.ChatMemberStatus.OWNER,
                        pyrogram.enums.ChatMemberStatus.ADMINISTRATOR,
                    ):
                        return await CallbackQuery.message.edit_text(
                            "ɪ ᴍᴜsᴛ ʙᴇ ᴀᴅᴍɪɴ ᴛᴏ ᴇxᴇᴄᴜᴛᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ"
                        )
                try:
                    await func(client, CallbackQuery)
                except pyrogram.errors.exceptions.forbidden_403.ChatAdminRequired:
                    pass
                except BaseException as e:
                    return await CallbackQuery.message.delete()
                           await CallbackQuery.message.reply_text(
                    "ᴀɴ ɪɴᴛᴇʀɴᴀʟ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ᴄᴏᴍᴍᴀɴᴅ\nᴇʀʀᴏʀ {e}\n"
                )

            self.add_handler(
                pyrogram.handlers.CallbackQueryHandler(decorator, filter)
            )
            return decorator

        return wrapper

Decorators.on_cb = callback