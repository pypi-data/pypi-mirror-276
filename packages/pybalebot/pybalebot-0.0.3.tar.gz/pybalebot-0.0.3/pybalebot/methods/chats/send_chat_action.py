import pybalebot
from typing import Union


class SendChatAction:
    async def send_chat_action(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            action: str = 'typing'
    ):
        data = dict(chat_id=chat_id, action=action)
        return await self.api.execute('sendChatAction', data=data)