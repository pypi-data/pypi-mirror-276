from typing import Union
import pybalebot

class GetChatMemberCount:
    async def get_chat_member_count(
            self: "pybalebot.Client",
            chat_id: Union[str, int]
    ):
        return await self.api.execute('getChatMemberCount', data=dict(chat_id=chat_id))