from pybalebot.types import InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo
from typing import List, Union, Optional
import pybalebot


class SendMediaGroup:
    async def send_media_group(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            media: List[Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]],
            reply_to_message_id: Optional[int] = None
    ) -> List[dict]:
        """Send a group of photos, videos, documents, or audios as an album.

        Args:
            chat_id (Union[str, int]): Unique identifier for the target chat or username of the target channel.
            media (List[Union[InputMediaAudio, InputMediaDocument, InputMediaPhoto, InputMediaVideo]]): An array of InputMedia objects describing the media to be sent.
            reply_to_message_id (Optional[int], optional): If the message is a reply, ID of the original message. Defaults to None.

        Returns:
            List[dict]: On success, an array of the sent Messages is returned.
        """
        data = {
            'chat_id': str(chat_id),
            'media': [m.to_dict() for m in media],
            'reply_to_message_id': reply_to_message_id,
        }
        return await self.api.execute('sendMediaGroup', data=data)
