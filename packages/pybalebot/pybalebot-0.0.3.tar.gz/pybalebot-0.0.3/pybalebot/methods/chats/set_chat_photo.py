from typing import Union
import pybalebot
import aiofiles
import aiohttp
import os


class SetChatPhoto:
    async def set_chat_photo(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            photo: str,
    ):
        if os.path.isfile(photo):
            async with aiofiles.open(photo, 'rb') as f:
                form = aiohttp.FormData()
                form.add_field('chat_id', str(chat_id))
                form.add_field('photo', await f.read(), filename=os.path.basename(photo))
            return await self.api.execute('setChatPhoto', form=form)
        else:
            data = {
                'chat_id': str(chat_id),
                'photo': photo
            }
            return await self.api.execute('setChatPhoto', data=data)