from .send_message import SendMessage
from .edit_message_text import EditMessageText
from .send_photo import SendPhoto
from .copy_message import CopyMessage
from .delete_message import DeleteMessage
from .forward_message import ForwardMessage
from .send_document import SendDocument
from .send_audio import SendAudio
from .send_video import SendVideo
from .send_animation import SendAnimation
from .send_voice import SendVoice
from .send_location import SendLocation
from .send_contact import SendContact
from .send_media_group import SendMediaGroup
from .pin_chat_message import PinChatMessage
from .send_poll import SendPoll
from .edit_message_caption import EditMessageCaption

class Messages(
    SendMessage,
    EditMessageText,
    SendPhoto,
    CopyMessage,
    DeleteMessage,
    ForwardMessage,
    SendDocument,
    SendAudio,
    SendVideo,
    SendAnimation,
    SendVoice,
    SendLocation,
    SendContact,
    SendMediaGroup,
    PinChatMessage,
    SendPoll,
    EditMessageCaption
):
    pass