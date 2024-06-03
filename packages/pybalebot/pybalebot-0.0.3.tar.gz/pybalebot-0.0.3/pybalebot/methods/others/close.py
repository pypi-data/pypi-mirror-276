import pybalebot

class Close:
    async def close(self: "pybalebot.Client"):
        return await self.api.execute('close')