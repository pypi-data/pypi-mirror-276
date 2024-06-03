from typing import Union
import pybalebot

class GetChatMembersCount:
    async def get_chat_members_count(
            self: "pybalebot.Client",
            chat_id: Union[str, int]
    ):
        return await self.api.execute('getChatMembersCount', data=dict(chat_id=chat_id))