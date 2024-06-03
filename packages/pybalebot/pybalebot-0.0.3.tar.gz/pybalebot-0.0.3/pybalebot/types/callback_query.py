import json
import pybalebot
from typing import Optional, Union

from pybalebot.types.inline_keyboard_markup import InlineKeyboardMarkup
from pybalebot.types.reply_keyboard_markup import ReplyKeyboardMarkup
from pybalebot.types.reply_keyboard_remove import ReplyKeyboardRemove


class CallbackQuery:
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
                update[index] = CallbackQuery(update=element)
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
                        update = CallbackQuery(update=update)
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
    def inline_message_id(self) -> str:
        return self.find_keys('inline_message_id')

    @property
    def message_id(self):
        return self.find_keys(keys=['message_id', 'pinned_message_id'])

    @property
    def reply_message_id(self):
        return self.message.find_keys(keys='reply_to_message_id')

    @property
    def data(self) -> str:
        return self.find_keys('data')

    async def answer(
            self,
            text: str,
            show_alert: bool = False,
            url: str = None,
            cache_time: int = 0
    ):
        return await self.client.answer_callback_query(
            callback_query_id=self.id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time
        )