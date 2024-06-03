from .get_me import GetMe
from .get_user_profile_photos import GetUserProfilePhotos

class Users(
    GetMe,
    GetUserProfilePhotos
):
    pass