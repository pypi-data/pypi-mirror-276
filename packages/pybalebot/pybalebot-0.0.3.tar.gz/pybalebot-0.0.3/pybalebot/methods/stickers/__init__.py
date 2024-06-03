from .upload_sticker_file import UploadStickerFile
from .create_new_sticker_set import CreateNewStickerSet
from .add_sticker_to_set import AddStickerToSet

class Stickers(
    UploadStickerFile,
    CreateNewStickerSet,
    AddStickerToSet
):
    pass