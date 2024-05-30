from typing import Union
import pybalebot

class GetChat:
    async def get_chat(self: "pybalebot.Client", chat_id: Union[str, int]):
        data = dict(chat_id=chat_id)
        return await self.api.execute('getChat', data=data)