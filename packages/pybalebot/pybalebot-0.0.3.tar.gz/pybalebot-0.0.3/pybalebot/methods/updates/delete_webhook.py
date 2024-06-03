import pybalebot

class DeleteWebhook:
    async def delete_webhook(self: "pybalebot.Client", url: str = None):
        return await self.api.execute('deleteWebhook')