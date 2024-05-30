from typing import Optional

class InlineKeyboardButton:
    def __init__(self, text: str, callback_data: Optional[str] = None, url: Optional[str] = None):
        self.text = text
        self.callback_data = callback_data
        self.url = url

    def to_dict(self):
        data = {'text': self.text}
        if self.callback_data:
            data['callback_data'] = self.callback_data
        if self.url:
            data['url'] = self.url
        return data