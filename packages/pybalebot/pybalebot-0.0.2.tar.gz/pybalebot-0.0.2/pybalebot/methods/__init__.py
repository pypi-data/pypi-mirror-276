from .updates import Updates
from .messages import Messages
from .users import Users
from .chats import Chats


class Methods(
    Updates,
    Users,
    Messages,
    Chats
):
    pass