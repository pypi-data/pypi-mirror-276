import pybalebot

class SetWebHook:
    async def set_webhook(self: "pybalebot.Client", url: str = None):
        return await self.api.execute('setWebhook', data=dict(url=url))