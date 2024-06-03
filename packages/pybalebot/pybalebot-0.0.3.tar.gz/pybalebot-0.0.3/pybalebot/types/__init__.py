from .results import Results
from .message import Message
from .inline_keyboard_button import InlineKeyboardButton
from .inline_keyboard_markup import InlineKeyboardMarkup
from .reply_keyboard_remove import ReplyKeyboardRemove
from .keyboard_button import KeyboardButton
from .reply_keyboard_markup import ReplyKeyboardMarkup
from .input_file import InputMedia
from .input_media_animation import InputMediaAnimation
from .input_media_photo import InputMediaPhoto
from .input_media_video import InputMediaVideo
from .input_media_document import InputMediaDocument
from .input_media_audio import InputMediaAudio
from .inline_query_result import InlineQueryResult
from .callback_query import CallbackQuery

from typing import Optional, Dict


class InputMessageContent:
    """Base class for input message content."""
    def to_dict(self) -> Dict:
        raise NotImplementedError


class InputTextMessageContent(InputMessageContent):
    def __init__(self, message_text: str):
        self.message_text = message_text

    def to_dict(self) -> Dict:
        return {'message_text': self.message_text}

class InlineQueryResultArticle(InlineQueryResult):
    def __init__(self, id: str, title: str, input_message_content: InputMessageContent):
        self.id = id
        self.title = title
        self.input_message_content = input_message_content

    def to_dict(self) -> Dict:
        return {
            'type': 'article',
            'id': self.id,
            'title': self.title,
            'input_message_content': self.input_message_content.to_dict()
        }


class InlineQueryResultPhoto(InlineQueryResult):
    def __init__(self, id: str, photo_url: str, thumb_url: str, caption: Optional[str] = None):
        self.id = id
        self.photo_url = photo_url
        self.thumb_url = thumb_url
        self.caption = caption

    def to_dict(self) -> Dict:
        data = {
            'type': 'photo',
            'id': self.id,
            'photo_url': self.photo_url,
            'thumb_url': self.thumb_url,
        }
        if self.caption:
            data['caption'] = self.caption
        return data


class InlineQueryResultVideo(InlineQueryResult):
    def __init__(self, id: str, video_url: str, mime_type: str, thumb_url: str, title: str, caption: Optional[str] = None):
        self.id = id
        self.video_url = video_url
        self.mime_type = mime_type
        self.thumb_url = thumb_url
        self.title = title
        self.caption = caption

    def to_dict(self) -> Dict:
        data = {
            'type': 'video',
            'id': self.id,
            'video_url': self.video_url,
            'mime_type': self.mime_type,
            'thumb_url': self.thumb_url,
            'title': self.title,
        }
        if self.caption:
            data['caption'] = self.caption
        return data

