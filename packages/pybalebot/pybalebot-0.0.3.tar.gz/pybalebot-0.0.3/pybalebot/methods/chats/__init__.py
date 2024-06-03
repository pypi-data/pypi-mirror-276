from .unban_chat_member import UnbanChatMember
from .ban_chat_member import BanChatMember
from .promote_chat_member import PromoteChatMember
from .set_chat_photo import SetChatPhoto
from .leave_chat import LeaveChat
from .get_chat import GetChat
from .get_chat_member_count import GetChatMembersCount
from .get_chat_administrators import GetChatAdministrators
from .export_chat_invite_link import ExportChatInviteLink
from .get_chat_member import GetChatMember
from .send_chat_action import SendChatAction


class Chats(
    UnbanChatMember,
    BanChatMember,
    PromoteChatMember,
    SetChatPhoto,
    LeaveChat,
    GetChat,
    GetChatMembersCount,
    GetChatAdministrators,
    ExportChatInviteLink,
    GetChatMember,
    SendChatAction
):
    pass