from typing import Optional, Union
import pybalebot
from pybalebot.types.inline_keyboard_markup import InlineKeyboardMarkup
from pybalebot.types.reply_keyboard_markup import ReplyKeyboardMarkup
from pybalebot.types.reply_keyboard_remove import ReplyKeyboardRemove

class EditMessageCaption:
    async def edit_message_caption(self: "pybalebot.Client", caption: str, chat_id: Union[str, int] = None, message_id: int = None, reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove]] = None):
        data = dict(
            caption=caption,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup
        )
        return await self.api.execute('editMessageCaption', data=data)