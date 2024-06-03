import pybalebot
from typing import Optional, Union
from pybalebot.types.inline_keyboard_markup import InlineKeyboardMarkup
from pybalebot.types.reply_keyboard_markup import ReplyKeyboardMarkup
from pybalebot.types.reply_keyboard_remove import ReplyKeyboardRemove


class SendLocation:
    async def send_location(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            latitude: float,
            longitude: float,
            horizontal_accuracy: Optional[float] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove]] = None
    ) -> dict:
        """Send a location.

        Args:
            chat_id (Union[str, int]): Unique identifier for the target chat or username of the target channel.
            latitude (float): Latitude of the location.
            longitude (float): Longitude of the location.
            horizontal_accuracy (Optional[float], optional): The radius of uncertainty for the location, measured in meters; 0-1500. Defaults to None.
            reply_to_message_id (Optional[int], optional): If the message is a reply, ID of the original message. Defaults to None.
            reply_markup (Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove]], optional): Additional interface options. Defaults to None.

        Returns:
            dict: On success, the sent Message is returned.
        """
        data = {
            'chat_id': str(chat_id),
            'latitude': latitude,
            'longitude': longitude,
            'horizontal_accuracy': horizontal_accuracy,
            'reply_to_message_id': reply_to_message_id,
            'reply_markup': reply_markup,
        }
        return await self.api.execute('sendLocation', data=data)
