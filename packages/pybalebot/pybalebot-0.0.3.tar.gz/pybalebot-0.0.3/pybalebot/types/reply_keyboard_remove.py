class ReplyKeyboardRemove:
    def __init__(self, remove_keyboard: bool = True, selective: bool = False):
        self.remove_keyboard = remove_keyboard
        self.selective = selective

    def to_dict(self):
        return {
            'remove_keyboard': self.remove_keyboard,
            'selective': self.selective
        }