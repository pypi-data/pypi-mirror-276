import pybalebot

class GetFile:
    async def get_file(self: "pybalebot.Client", file_id: str):
        return await self.api.execute('getFile', data=dict(file_id=file_id))