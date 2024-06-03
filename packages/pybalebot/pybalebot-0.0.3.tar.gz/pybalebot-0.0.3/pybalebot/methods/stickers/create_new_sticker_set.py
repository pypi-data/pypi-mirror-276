import pybalebot


class CreateNewStickerSet:
    async def create_new_sticker_set(
            self: "pybalebot.Client",
            user_id: int,
            name: str,
            title: str,
            stickers: list
    ) -> bool:
        """Create a new sticker set.

        Args:
            user_id (int): The user ID of the sticker set owner.
            name (str): The short name of the sticker set, used in URLs (e.g., animals).
            title (str): The title of the sticker set.
            stickers (list): A list of InputSticker objects representing the stickers to be added to the sticker set.

        Returns:
            bool: True if the sticker set is created successfully, False otherwise.
        """
        data = {
            'user_id': user_id,
            'name': name,
            'title': title,
            'stickers': stickers
        }
        return await self.api.execute('createNewStickerSet', data=data)