import json
import pybalebot
from typing import List, Optional, Union

from pybalebot.types.inline_keyboard_markup import InlineKeyboardMarkup
from pybalebot.types.input_media_photo import InputMediaPhoto
from pybalebot.types.input_media_video import InputMediaVideo
from pybalebot.types.reply_keyboard_markup import ReplyKeyboardMarkup
from pybalebot.types.reply_keyboard_remove import ReplyKeyboardRemove


class Message:
    def __str__(self) -> str:
        return self.jsonify(indent=2)

    def __getattr__(self, name):
        return self.find_keys(keys=name)

    def __setitem__(self, key, value):
        self.original_update[key] = value

    def __getitem__(self, key):
        return self.original_update[key]

    def __lts__(self, update: list, *args, **kwargs):
        for index, element in enumerate(update):
            if isinstance(element, list):
                update[index] = self.__lts__(update=element)
            elif isinstance(element, dict):
                update[index] = Message(update=element)
            else:
                update[index] = element
        return update

    def __init__(self, update: dict, *args, **kwargs) -> None:
        self.client: "pybalebot.Client" = update.get('client')
        self.original_update = update

    def jsonify(self, indent=None) -> str:
        result = self.original_update
        result['original_update'] = 'dict{...}'
        return json.dumps(result, indent=indent, ensure_ascii=False, default=lambda value: str(value))

    def find_keys(self, keys, original_update=None, *args, **kwargs):
        if original_update is None:
            original_update = self.original_update

        if not isinstance(keys, list):
            keys = [keys]

        if isinstance(original_update, dict):
            for key in keys:
                try:
                    update = original_update[key]
                    if isinstance(update, dict):
                        update = Message(update=update)
                    elif isinstance(update, list):
                        update = self.__lts__(update=update)
                    return update
                except KeyError:
                    pass
            original_update = original_update.values()

        for value in original_update:
            if isinstance(value, (dict, list)):
                try:
                    return self.find_keys(keys=keys, original_update=value)
                except AttributeError:
                    return None

        return None

    @property
    def command(self):
        return self.find_keys('command')

    @property
    def to_dict(self) -> dict:
        "Return the update as dict"
        return self.original_update

    @property
    def message(self):
        return self.find_keys('message')

    @property
    def is_me(self):
        return self.find_keys('from').id == self.client.me.id

    @property
    def text(self) -> str:
        return self.message.text

    @property
    def message_id(self):
        return self.find_keys(keys=['message_id', 'pinned_message_id'])

    @property
    def reply_message_id(self):
        return self.message.find_keys(keys='reply_to_message_id')

    async def reply(
            self,
            text: str,
            chat_id: int=None,
            reply_to_message_id: int = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove]] = None
        ):
        if chat_id is None:
            chat_id = self['chat']['id']
        if reply_to_message_id is None:
            reply_to_message_id = self['message_id'] if self['chat']['type'] != 'group' else None

        result = await self.client.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )
        result['client'] = self.client
        return Message(result.original_update)

    async def reply_text(self, text: str, chat_id: int=None, reply_to_message_id: int = None):
        result = await self.client.send_message(chat_id or self.chat.id, text, reply_to_message_id=reply_to_message_id or self.message_id)
        result['client'] = self.client
        return Message(result.original_update)

    async def edit_text(self, text: str, chat_id: int=None, message_id: int = None):
        result = await self.client.edit_message_text(text, chat_id or self.chat.id, message_id=message_id or self.message_id)
        result['client'] = self.client
        return Message(result.original_update)

    async def ban_member(self, chat_id: Union[str, int] = None, user_id: int = None):
        return await self.client.ban_chat_member(chat_id or self.chat.id, user_id or self.find_keys('from').id)

    async def unban_member(
            self,
            chat_id: Union[str, int] = None,
            user_id: int = None,
            only_if_banned: bool = None
    ):
        return await self.client.unban_chat_member(chat_id or self.chat.id, user_id or self.find_keys('from').id, only_if_banned=only_if_banned)

    async def delete(self, chat_id: Union[str, int] = None, message_id: int = None):
        return await self.client.delete_message(chat_id or self.chat.id, message_id or self.message_id)
    
    async def reply_media_group(
            self,
            chat_id: Union[str, int],
            media: List[Union[InputMediaPhoto, InputMediaVideo]],
            reply_to_message_id: int = None
    ):
        result = await self.client.send_media_group(chat_id=chat_id or self.chat.id, media=media, reply_to_message_id=reply_to_message_id or self.message_id)
        result['client'] = self.client
        return Message(result.original_update)
    
    async def reply_photo(
            self,
            chat_id: Union[str, int],
            photo: str,
            reply_to_message_id: int = None,
            reply_markup: Union["InlineKeyboardMarkup", "ReplyKeyboardMarkup", "ReplyKeyboardRemove"] = None
    ):
        result = await self.client.send_photo(chat_id=chat_id or self.chat.id, photo=photo, reply_to_message_id=reply_to_message_id or self.message_id, reply_markup=reply_markup)
        result['client'] = self.client
        return Message(result.original_update)
    
    async def reply_audio(
            self,
            chat_id: Union[str, int],
            audio: str,
            reply_to_message_id: int = None,
            reply_markup: Union["InlineKeyboardMarkup", "ReplyKeyboardMarkup", "ReplyKeyboardRemove"] = None
    ):
        result = await self.client.send_audio(chat_id=chat_id or self.chat.id, audio=audio, reply_to_message_id=reply_to_message_id or self.message_id, reply_markup=reply_markup)
        result['client'] = self.client
        return Message(result.original_update)
    
    async def reply_animation(
            self,
            chat_id: Union[str, int],
            animation: str,
            reply_to_message_id: int = None,
            reply_markup: Union["InlineKeyboardMarkup", "ReplyKeyboardMarkup", "ReplyKeyboardRemove"] = None
    ):
        result = await self.client.send_animation(chat_id=chat_id or self.chat.id, animation=animation, reply_to_message_id=reply_to_message_id or self.message_id, reply_markup=reply_markup)
        result['client'] = self.client
        return Message(result.original_update)
    
    async def reply_video(
            self,
            chat_id: Union[str, int],
            video: str,
            reply_to_message_id: int = None,
            reply_markup: Union["InlineKeyboardMarkup", "ReplyKeyboardMarkup", "ReplyKeyboardRemove"] = None
    ):
        result = await self.client.send_video(chat_id=chat_id or self.chat.id, video=video, reply_to_message_id=reply_to_message_id or self.message_id, reply_markup=reply_markup)
        result['client'] = self.client
        return Message(result.original_update)
    
    async def reply_document(
            self,
            chat_id: Union[str, int],
            document: str,
            caption: str = None,
            reply_to_message_id: int = None,
            reply_markup: Union["InlineKeyboardMarkup", "ReplyKeyboardMarkup", "ReplyKeyboardRemove"] = None
    ):
        result = await self.client.send_document(chat_id=chat_id or self.chat.id, document=document, caption=caption, reply_to_message_id=reply_to_message_id or self.message_id, reply_markup=reply_markup)
        result['client'] = self.client
        return Message(result.original_update)
    
    async def reply_voice(
            self,
            chat_id: Union[str, int],
            voice: str,
            caption: str = None,
            reply_to_message_id: int = None,
            reply_markup: Union["InlineKeyboardMarkup", "ReplyKeyboardMarkup", "ReplyKeyboardRemove"] = None
    ):
        result = await self.client.send_voice(chat_id=chat_id or self.chat.id, voice=voice, caption=caption, reply_to_message_id=reply_to_message_id or self.message_id, reply_markup=reply_markup)
        result['client'] = self.client
        return Message(result.original_update)
    
    async def reply_contact(
            self,
            chat_id: Union[str, int],
            phone_number: int,
            first_name: str,
            last_name: str = None,
            reply_to_message_id: int = None,
            reply_markup: Union["InlineKeyboardMarkup", "ReplyKeyboardMarkup", "ReplyKeyboardRemove"] = None
    ):
        result = await self.client.send_contact(
            chat_id=chat_id or self.chat.id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            reply_to_message_id=reply_to_message_id or self.message_id,
            reply_markup=reply_markup)
        result['client'] = self.client
        return Message(result.original_update)
    
    # async def reply_sticker(
    #         self,
    #         chat_id: Union[str, int],
    #         photo: str,
    #         reply_to_message_id: int = None,
    #         reply_markup: Union["InlineKeyboardMarkup", "ReplyKeyboardMarkup", "ReplyKeyboardRemove"] = None
    # ):
    #     result = await self.client.send_sticker(chat_id=chat_id or self.chat.id, photo=photo, reply_to_message_id=reply_to_message_id or self.message_id, reply_markup=reply_markup)
    #     result['client'] = self.client
    #     return Message(result.original_update)
    
    async def reply_poll(
            self,
            chat_id: Union[str, int],
            question: str,
            options: list,
            is_anonymous=True,
            type='regular',
            reply_to_message_id: int = None,
            reply_markup: Union["InlineKeyboardMarkup", "ReplyKeyboardMarkup", "ReplyKeyboardRemove"] = None
    ):
        result = await self.client.send_poll(chat_id=chat_id or self.chat.id, question=question, options=options, is_anonymous=is_anonymous, type=type, reply_to_message_id=reply_to_message_id or self.message_id, reply_markup=reply_markup)
        result['client'] = self.client
        return Message(result.original_update)
    
    async def get_member(
            self,
            chat_id: Union[str, int] = None,
            user_id: Union[str, int] = None
    ):
        try:
            result = await self.client.get_chat_member(
                chat_id=chat_id or self.chat.id,
                user_id=user_id or self.find_keys('from').id
            )
            result['client'] = self.client
            return Message(result.original_update)

        except Exception:
            pass

    async def download(
            self,
            file_id: str,
            file_name: str = None,
            in_memory: bool = False,
            progress = None,
            progress_args = (),
            save: bool = False
    ):
        return await self.client.download(
            file_id=file_id,
            file_name=file_name,
            in_memory=in_memory,
            progress=progress,
            progress_args=progress_args,
            save=save
        )

    async def forward(
            self,
            chat_id: Union[str, int],
            from_chat_id: Union[str, int] = None,
            message_id: int = None
    ):
        result = await self.client.forward_message(
            chat_id=chat_id or self.chat.id,
            from_chat_id=from_chat_id or self.chat.id,
            message_id=message_id or self.message_id

        )
        result['client'] = self.client
        return Message(result.original_update)

    async def copy(
            self,
            chat_id: Union[str, int],
            from_chat_id: Union[str, int] = None,
            message_id: int = None
    ):
        result = await self.client.copy_message(
            chat_id=chat_id or self.chat.id,
            from_chat_id=from_chat_id or self.chat.id,
            message_id=message_id or self.message_id

        )
        result['client'] = self.client
        return Message(result.original_update)