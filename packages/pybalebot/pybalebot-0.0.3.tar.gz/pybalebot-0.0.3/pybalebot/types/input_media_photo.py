from .input_file import InputMedia

class InputMediaPhoto(InputMedia):
    def __init__(self, media, caption=None, parse_mode=None):
        super().__init__('photo', media, caption, parse_mode)