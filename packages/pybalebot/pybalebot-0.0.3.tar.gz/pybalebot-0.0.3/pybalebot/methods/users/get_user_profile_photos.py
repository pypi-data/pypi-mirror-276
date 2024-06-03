from typing import Union, Optional
import pybalebot

class GetUserProfilePhotos:
    async def get_user_profile_photos(
            self: "pybalebot.Client",
            user_id: Union[int, str],
            offset: Optional[int] = None,
            limit: Optional[int] = None
    ) -> dict:
        """Get a list of profile pictures for a user.

        Args:
            user_id (Union[int, str]): Unique identifier of the target user.
            offset (Optional[int], optional): Sequential number of the first photo to be returned. Defaults to None.
            limit (Optional[int], optional): Limits the number of photos to be retrieved. Values between 1-100 are accepted. Defaults to None.

        Returns:
            dict: On success, returns a UserProfilePhotos object.
        """
        data = {
            'user_id': user_id,
            'offset': offset,
            'limit': limit
        }
        return await self.api.execute('getUserProfilePhotos', data=data)
