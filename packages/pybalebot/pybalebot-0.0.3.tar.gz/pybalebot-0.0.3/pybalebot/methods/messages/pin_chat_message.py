import pybalebot
from typing import Union

class PinChatMessage:
    async def pin_chat_message(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            message_id: int,
            disable_notification : bool = False
    ):
        data = dict(chat_id=chat_id, message_id=message_id, disable_notification=disable_notification)
        return await self.api.execute('pinChatMessage', data=data)