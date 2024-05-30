import pybalebot
from typing import Union

class UnbanChatMember:
    async def unban_chat_member(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            user_id: int,
            only_if_banned: bool = None
    ):
        data = dict(chat_id=chat_id, user_id=user_id)
        if only_if_banned is not None:
            data['only_if_banned'] = only_if_banned
        return await self.api.execute('unbanChatMember', data=data)