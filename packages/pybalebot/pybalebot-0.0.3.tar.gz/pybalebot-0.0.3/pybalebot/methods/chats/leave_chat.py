from typing import Union
import pybalebot

class LeaveChat:
    async def leave_chat(
            self: "pybalebot.Client",
            chat_id: Union[str, int]
    ):
        data = dict(chat_id=chat_id)
        return await self.api.execute('leaveChat', data=data)