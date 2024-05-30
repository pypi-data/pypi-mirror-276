from typing import List
from .keyboard_button import KeyboardButton

class ReplyKeyboardMarkup:
    def __init__(self, keyboard: List[List[KeyboardButton]], resize_keyboard: bool = False, one_time_keyboard: bool = False, selective: bool = False):
        self.keyboard = keyboard
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard
        self.selective = selective

    def to_dict(self):
        return {
            'keyboard': [[button.to_dict() for button in row] for row in self.keyboard],
            'resize_keyboard': self.resize_keyboard,
            'one_time_keyboard': self.one_time_keyboard,
            'selective': self.selective
        }