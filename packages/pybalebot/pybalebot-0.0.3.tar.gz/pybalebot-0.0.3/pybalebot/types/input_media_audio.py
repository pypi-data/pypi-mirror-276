from .input_file import InputMedia

class InputMediaAudio(InputMedia):
    def __init__(self, media, caption=None, parse_mode=None, thumbnail=None, duration=None, title=None):
        super().__init__('audio', media, caption, parse_mode, thumbnail, duration=duration, title=title)
