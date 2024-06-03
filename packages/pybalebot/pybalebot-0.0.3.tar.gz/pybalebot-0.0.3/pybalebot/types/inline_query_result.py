class InlineQueryResult:
    def __init__(self, type: str, id: str):
        self.type = type
        self.id = id
        self.title = None
        self.input_message_content = None
        self.caption = None
        self.reply_markup = None
        self.parse_mode = None
        self.thumb_url = None
        self.photo_url = None
        self.document_url = None
        self.document_title = None
        self.video_url = None
        self.video_title = None
        # Add more attributes as needed for different types of results

    def set_title(self, title: str):
        self.title = title

    def set_input_message_content(self, input_message_content):
        self.input_message_content = input_message_content

    def set_caption(self, caption: str):
        self.caption = caption

    def set_reply_markup(self, reply_markup):
        self.reply_markup = reply_markup

    def set_parse_mode(self, parse_mode: str):
        self.parse_mode = parse_mode

    def set_thumb_url(self, thumb_url: str):
        self.thumb_url = thumb_url

    def set_photo_url(self, photo_url: str):
        self.photo_url = photo_url

    def set_document_url(self, document_url: str, document_title: str = None):
        self.document_url = document_url
        if document_title:
            self.document_title = document_title

    def set_video_url(self, video_url: str, video_title: str = None):
        self.video_url = video_url
        if video_title:
            self.video_title = video_title

    def to_dict(self):
        result_dict = {
            "type": self.type,
            "id": self.id
        }
        if self.title:
            result_dict["title"] = self.title
        if self.input_message_content:
            result_dict["input_message_content"] = self.input_message_content
        if self.caption:
            result_dict["caption"] = self.caption
        if self.reply_markup:
            result_dict["reply_markup"] = self.reply_markup
        if self.parse_mode:
            result_dict["parse_mode"] = self.parse_mode
        if self.thumb_url:
            result_dict["thumb_url"] = self.thumb_url
        if self.photo_url:
            result_dict["photo_url"] = self.photo_url
        if self.document_url:
            result_dict["document_url"] = self.document_url
        if self.document_title:
            result_dict["document_title"] = self.document_title
        if self.video_url:
            result_dict["video_url"] = self.video_url
        if self.video_title:
            result_dict["video_title"] = self.video_title
        return result_dict