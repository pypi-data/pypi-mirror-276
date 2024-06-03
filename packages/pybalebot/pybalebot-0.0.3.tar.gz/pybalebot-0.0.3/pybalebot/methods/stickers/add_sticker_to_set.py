import pybalebot


class AddStickerToSet:
    async def add_sticker_to_set(
            self: "pybalebot.Client",
            user_id: int,
            name: str,
            sticker: dict
    ) -> bool:
        """Add a new sticker to a sticker set.

        Args:
            user_id (int): The user ID of the sticker set owner.
            name (str): The name of the sticker set.
            sticker (dict): A JSON-serialized object containing information about the sticker to be added.
                If the exact sticker is already added to the set, the sticker set won't be modified.

        Returns:
            bool: True if the sticker is added successfully, False otherwise.
        """
        data = {
            'user_id': user_id,
            'name': name,
            'sticker': sticker if isinstance(sticker, dict) else sticker.to_dict
        }
        return await self.api.execute('addStickerToSet', data=data)