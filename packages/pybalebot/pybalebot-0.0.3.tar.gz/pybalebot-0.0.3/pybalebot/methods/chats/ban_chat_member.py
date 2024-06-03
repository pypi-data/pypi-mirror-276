from typing import Union
import pybalebot

class BanChatMember:
    async def ban_chat_member(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            user_id: int
    ):
        data = dict(chat_id=chat_id, user_id=user_id)
        return await self.api.execute('banChatMember', data=data)