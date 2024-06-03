import aiohttp
import pybalebot.api
import aiofiles
import os

class InputMedia:
    def __init__(self, type: str, media: str, caption: str = None, thumbnail: str = None, width: int = None, height: int = None, duration: int = None, title: str = None):
        self.type = type
        self.media = media
        self.caption = caption
        self.thumbnail = thumbnail
        self.width = width
        self.height = height
        self.duration = duration
        self.title = title

    def to_dict(self):
        data = {
            'type': self.type,
            'media': self.media
        }

        if self.caption:
            data['caption'] = self.caption
        if self.thumbnail:
            data['thumbnail'] = self.thumbnail
        if self.width:
            data['width'] = self.width
        if self.height:
            data['height'] = self.height
        if self.duration:
            data['duration'] = self.duration
        if self.title:
            data['title'] = self.title
        return data

    async def upload_media(self, method: str, api: "pybalebot.api.BaleAPI"):
        if os.path.isfile(self.media):  # Check if the file exists in the local storage
            form = aiohttp.FormData()
            async with aiofiles.open(self.media, 'rb') as f:
                form.add_field('file', await f.read(), filename=os.path.basename(self.media))
            return await api.execute(method, form=form)
        else:
            raise FileNotFoundError(f"Media file not found: {self.media}")

    async def upload_thumbnail(self, method: str, api: "pybalebot.api.BaleAPI"):
        if self.thumbnail and os.path.isfile(self.thumbnail):  # Check if the thumbnail exists in the local storage
            form = aiohttp.FormData()
            async with aiofiles.open(self.thumbnail, 'rb') as f:
                form.add_field('file', await f.read(), filename=os.path.basename(self.thumbnail))
            return await api.execute(method, form=form)
