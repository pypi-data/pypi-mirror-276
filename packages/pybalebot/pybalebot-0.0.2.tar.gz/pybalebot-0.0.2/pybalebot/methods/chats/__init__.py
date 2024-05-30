from .unban_chat_member import UnbanChatMember
from .ban_chat_member import BanChatMember
from .promote_chat_member import PromoteChatMember
from .set_chat_photo import SetChatPhoto
from .leave_chat import LeaveChat
from .get_chat import GetChat
from .get_chat_member_count import GetChatMemberCount
from .get_chat_administrators import GetChatAdministrators


class Chats(
    UnbanChatMember,
    BanChatMember,
    PromoteChatMember,
    SetChatPhoto,
    LeaveChat,
    GetChat,
    GetChatMemberCount,
    GetChatAdministrators
):
    pass