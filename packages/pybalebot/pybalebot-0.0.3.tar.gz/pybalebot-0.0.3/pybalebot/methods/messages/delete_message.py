from typing import Union
import pybalebot

class DeleteMessage:
    async def delete_message(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            message_id: int
    ):
        data = dict(chat_id=chat_id, message_id=message_id)
        return await self.api.execute('deleteMessage', data=data)