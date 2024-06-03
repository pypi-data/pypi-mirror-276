from pybalebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from typing import Optional, Union
import pybalebot
import aiohttp
import aiofiles
import os


class SendAnimation:
    async def send_animation(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            animation: str,
            caption: Optional[str] = None,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove]] = None
    ) -> dict:
        """Send a document.

        Args:
            chat_id (Union[str, int]): Unique identifier for the target chat or username of the target channel.
            animation (str): File path of the document to be sent.
            caption (Optional[str], optional): Caption for the document, 0-1024 characters. Defaults to None.
            reply_to_message_id (Optional[int], optional): If the message is a reply, ID of the original message. Defaults to None.
            reply_markup (Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove]], optional): Additional interface options. Defaults to None.

        Returns:
            dict: On success, the sent Message is returned.
        """
        if os.path.isfile(animation):
            async with aiofiles.open(animation, 'rb') as f:
                form = aiohttp.FormData()
                form.add_field('chat_id', str(chat_id))
                form.add_field('caption', caption or '')
                form.add_field('reply_to_message_id', reply_to_message_id or '')
                if reply_markup is not None:
                    form.add_field('reply_markup', reply_markup.to_dict())
                form.add_field('animation', await f.read(), filename=os.path.basename(animation))
            return await self.api.execute('sendAnimation', form=form)
        else:
            data = {
                'chat_id': str(chat_id),
                'animation': animation,
                'caption': caption,
                'reply_to_message_id': reply_to_message_id,
                'reply_markup': reply_markup,
            }
            return await self.api.execute('sendAnimation', data=data)