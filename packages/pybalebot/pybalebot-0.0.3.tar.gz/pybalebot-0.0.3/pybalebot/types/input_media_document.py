from .input_file import InputMedia

class InputMediaDocument(InputMedia):
    def __init__(self, media, caption=None, parse_mode=None, thumbnail=None):
        super().__init__('document', media, caption, parse_mode, thumbnail)