from typing import Union
import pybalebot


class SetChatPhoto:
    async def set_chat_photo(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            photo: str,
    ):
        data = dict(chat_id=chat_id, photo=photo)
        return await self.api.execute('setChatPhoto', data=data)