from typing import Union
import pybalebot

class GetChatAdministrators:
    async def get_chat_administrators(
            self: "pybalebot.Client",
            chat_id: Union[int, str]
    ):
        return await self.api.execute('getChatAdministrators', data=dict(chat_id=chat_id))