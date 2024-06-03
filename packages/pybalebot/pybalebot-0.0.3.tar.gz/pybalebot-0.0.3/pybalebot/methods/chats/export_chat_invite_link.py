from typing import Union
import pybalebot

class ExportChatInviteLink:
    async def export_chat_invite_link(
            self: "pybalebot.Client",
            chat_id: Union[str, int]
    ):
        data = dict(chat_id=chat_id)
        return await self.api.execute('exportChatInviteLink', data=data)