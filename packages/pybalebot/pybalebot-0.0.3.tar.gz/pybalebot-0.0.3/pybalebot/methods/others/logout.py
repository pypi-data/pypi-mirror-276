import pybalebot

class Logout:
    async def logout(self: "pybalebot.Client"):
        return await self.api.execute('logout')