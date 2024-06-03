from typing import Optional, Union
import pybalebot
from pybalebot.types.inline_keyboard_markup import InlineKeyboardMarkup
from pybalebot.types.reply_keyboard_markup import ReplyKeyboardMarkup
from pybalebot.types.reply_keyboard_remove import ReplyKeyboardRemove


class SendContact:
    async def send_contact(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            phone_number: int,
            first_name: str,
            last_name: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove]] = None
    ) -> dict:
        """Send a contact.

        Args:
            chat_id (Union[str, int]): Unique identifier for the target chat or username of the target channel.
            phone_number (int): Contact's phone number.
            first_name (str): Contact's first name.
            last_name (Optional[str], optional): Contact's last name. Defaults to None.
            reply_to_message_id (Optional[int], optional): If the message is a reply, ID of the original message. Defaults to None.
            reply_markup (Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove]], optional): Additional interface options. Defaults to None.

        Returns:
            dict: On success, the sent Message is returned.
        """
        data = {
            'chat_id': str(chat_id),
            'phone_number': phone_number,
            'first_name': first_name,
            'last_name': last_name,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup,
        }
        return await self.api.execute('sendContact', data=data)
