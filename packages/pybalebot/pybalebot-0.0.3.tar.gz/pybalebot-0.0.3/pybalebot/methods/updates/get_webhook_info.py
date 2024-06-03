import pybalebot

class GetWebhookInfo:
    async def get_webhook_info(self: "pybalebot.Client"):
        return await self.api.execute('getWebhookInfo')