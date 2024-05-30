import pybalebot
from typing import Optional, Union

from pybalebot.types import InlineKeyboardMarkup
from pybalebot.types import ReplyKeyboardMarkup
from pybalebot.types import ReplyKeyboardRemove

class SendMessage:
    async def send_message(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            text: str,
            reply_to_message_id: int = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove]] = None
    ):
        data = dict(chat_id=chat_id,
                    text=text,
                    reply_to_message_id=reply_to_message_id,
                    reply_markup=reply_markup)
        return await self.api.execute('sendMessage', data=data)