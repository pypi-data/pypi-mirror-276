from .updates import Updates
from .messages import Messages
from .users import Users
from .chats import Chats
from .invoices import Invoices
from .others import Others


class Methods(
    Updates,
    Users,
    Messages,
    Chats,
    Invoices,
    Others
):
    pass