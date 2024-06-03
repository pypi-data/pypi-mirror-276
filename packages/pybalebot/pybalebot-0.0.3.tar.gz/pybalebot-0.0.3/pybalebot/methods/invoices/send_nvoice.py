import pybalebot
from typing import Union
from pybalebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

class SendInvoice:
    async def send_invoice(
            self: "pybalebot.Client",
            chat_id: int,
            title: str,
            description: str,
            payload: str,
            provider_token: str,
            prices: list,
            photo_url: str = None,
            reply_to_message_id: int = None,
            reply_markup: Union[ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup] = None
    ):
        data = {
            'chat_id': chat_id,
            'title': title,
            'description': description,
            'payload': payload,
            'provider_token': provider_token,
            'prices': prices,
            'photo_url': photo_url,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup
        }

        return await self.api.execute('sendInvoice', data=data)
