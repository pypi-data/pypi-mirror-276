class KeyboardButton:
    def __init__(self, text: str, request_contact: bool = False, request_location: bool = False):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location

    def to_dict(self):
        return {
            'text': self.text,
            'request_contact': self.request_contact,
            'request_location': self.request_location
        }