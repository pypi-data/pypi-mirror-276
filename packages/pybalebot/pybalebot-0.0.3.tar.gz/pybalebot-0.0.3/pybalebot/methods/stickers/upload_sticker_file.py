import pybalebot
import aiohttp
import aiofiles
import os

class UploadStickerFile:
    async def upload_sticker_file(
            self: "pybalebot.Client",
            user_id: int,
            sticker: str
    ) -> dict:
        """Upload a sticker file.

        Args:
            user_id (int): The user ID of the sticker owner.
            sticker (str): The file path or URL of the sticker to be uploaded. It should be in one of the formats .WEBP, .PNG, .TGS, or .WEBM.

        Returns:
            dict: The uploaded sticker file upon successful execution.
        """
        if os.path.isfile(sticker):
            async with aiofiles.open(sticker, 'rb') as f:
                form = aiohttp.FormData()
                form.add_field('user_id', str(user_id))
                form.add_field('sticker', await f.read(), filename=os.path.basename(sticker))
            return await self.api.execute('uploadStickerFile', form=form)
        elif isinstance(sticker, str) and sticker.startswith('http'):
            async with self.api.session.get(sticker) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    form = aiohttp.FormData()
                    form.add_field('user_id', str(user_id))
                    form.add_field('sticker', data, filename='sticker.png')
                    return await self.api.execute('uploadStickerFile', form=form)
                else:
                    raise aiohttp.ClientResponseError(f"Failed to download sticker from URL: {sticker}", status=resp.status)
        else:
            raise ValueError(f"Invalid sticker path or URL: {sticker}")
