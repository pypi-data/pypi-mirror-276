from typing import List

from .inline_keyboard_button import InlineKeyboardButton


class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard: List[List[InlineKeyboardButton]]):
        self.inline_keyboard = inline_keyboard

    def to_dict(self):
        return {'inline_keyboard': [[button.to_dict() for button in row] for row in self.inline_keyboard]}