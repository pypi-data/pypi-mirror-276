from .input_file import InputMedia

class InputMediaVideo(InputMedia):
    def __init__(self, media, caption=None, parse_mode=None, thumbnail=None, width=None, height=None, duration=None):
        super().__init__('video', media, caption, parse_mode, thumbnail, width, height, duration)