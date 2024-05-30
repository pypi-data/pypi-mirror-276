from .send_message import SendMessage
from .edit_message_text import EditMessageText
from .send_photo import SendPhoto
from .copy_message import CopyMessage
from .delete_message import DeleteMessage
from .forward_message import ForwardMessage

class Messages(
    SendMessage,
    EditMessageText,
    SendPhoto,
    CopyMessage,
    DeleteMessage,
    ForwardMessage
):
    pass