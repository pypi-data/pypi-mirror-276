import pybalebot
from typing import Union

class ForwardMessage:
    async def forward_message(
            self: "pybalebot.Client",
            chat_id: Union[int, str],
            from_chat_id: Union[int, str],
            message_id: int
    ):
        data = dict(
            chat_id=chat_id,
            from_chat_id=from_chat_id,
            message_id=message_id
        )
        return await self.api.execute('forwardMessage', data=data)