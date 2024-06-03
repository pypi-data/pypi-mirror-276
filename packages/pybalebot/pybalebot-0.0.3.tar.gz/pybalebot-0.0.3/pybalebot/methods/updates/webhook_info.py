import pybalebot

class WebhookInfo:
    async def webhook_info(self: "pybalebot.Client", url: str = None):
        return await self.api.execute('WebhookInfo', data=dict(url=url))