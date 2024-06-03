import pybalebot
from typing import Union, List, Optional, Literal

from pybalebot.types.inline_keyboard_markup import InlineKeyboardMarkup
from pybalebot.types.reply_keyboard_markup import ReplyKeyboardMarkup
from pybalebot.types.reply_keyboard_remove import ReplyKeyboardRemove


class SendPoll:
    async def send_poll(
            self: "pybalebot.Client",
            chat_id: Union[str, int],
            question: str,
            options: List[str],
            is_anonymous: Optional[bool] = True,
            type: Literal['regular', 'quiz'] = '',
            allows_multiple_answers: Optional[bool] = False,
            correct_option_id: Optional[int] = None,
            explanation: Optional[str] = None,
            explanation_parse_mode: Optional[str] = None,
            open_period: Optional[int] = None,
            close_date: Optional[int] = None,
            is_closed: Optional[bool] = False,
            disable_notification: Optional[bool] = False,
            reply_to_message_id: Optional[int] = None,
            reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove]] = None
    ):
        data = {
            'chat_id': chat_id,
            'question': question,
            'options': options,
            'is_anonymous': is_anonymous,
            'type': type,
            'allows_multiple_answers': allows_multiple_answers,
            'is_closed': is_closed
        }

        if correct_option_id is not None:
            data['correct_option_id'] = correct_option_id

        if explanation is not None:
            data['explanation'] = explanation

        if explanation_parse_mode is not None:
            data['explanation_parse_mode'] = explanation_parse_mode

        if open_period is not None:
            data['open_period'] = open_period

        if close_date is not None:
            data['close_date'] = close_date

        if disable_notification is not None:
            data['disable_notification'] = disable_notification

        if reply_to_message_id is not None:
            data['reply_to_message_id'] = reply_to_message_id

        if reply_markup is not None:
            data['reply_markup'] = reply_markup.to_dict()

        return await self.api.execute('sendPoll', data=data)
