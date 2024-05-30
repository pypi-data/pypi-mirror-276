from .get_updates import GetUpdates
from .set_webhook import SetWebHook
from .webhook_info import WebhookInfo
from .get_webhook_info import GetWebhookInfo

class Updates(
    GetUpdates,
    SetWebHook,
    WebhookInfo,
    GetWebhookInfo
):
    pass