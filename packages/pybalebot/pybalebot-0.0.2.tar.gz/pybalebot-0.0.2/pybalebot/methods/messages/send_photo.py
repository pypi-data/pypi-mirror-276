import pybalebot

from pybalebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from typing import Optional, Union

class SendPhoto:
    async def send_photo(
        self: "pybalebot.Client",
        chat_id: Union[int, str],
        photo: Union[str, bytes],
        caption: Optional[str] = None,
        from_chat_id: Union[int, str] = None,
        reply_to_message_id: Optional[int] = None,
        reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove]] = None
    ):
        """
        Send a photo to a chat.

        :param chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername).
        :param from_chat_id: Unique identifier for the chat where the original message was sent (or username of the channel in the format @channelusername).
        :param photo: Photo to send. Pass a file_id as String to send a photo that exists on the Bale servers (recommended), an HTTP URL as a String for Bale to get a photo from the internet, or upload a new photo using multipart/form-data.
        :param caption: Photo caption (0-1024 characters after entities parsing).
        :param reply_to_message_id: If the message is a reply, ID of the original message.
        :param reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove reply keyboard or to force a reply from the user.
        :return: On success, the sent Message is returned.
        """
        data = {
            'chat_id': chat_id,
            'from_chat_id': from_chat_id or chat_id,
            'photo': photo
        }
        if caption:
            data['caption'] = caption
        if reply_to_message_id:
            data['reply_to_message_id'] = reply_to_message_id
        if reply_markup:
            data['reply_markup'] = reply_markup.to_dict()

        return await self.api.execute('sendPhoto', data)