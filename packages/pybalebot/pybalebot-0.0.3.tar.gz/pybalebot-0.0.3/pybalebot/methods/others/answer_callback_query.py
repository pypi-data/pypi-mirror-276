from typing import Optional, Union
import pybalebot

class AnswerCallbackQuery:
    async def answer_callback_query(
            self: "pybalebot.Client",
            callback_query_id: str,
            text: Optional[str] = None,
            show_alert: Optional[bool] = None,
            url: Optional[str] = None,
            cache_time: Optional[int] = 0
    ) -> dict:
        """Send a response to a callback query.

        Args:
            callback_query_id (str): Unique identifier for the query to be answered.
            text (Optional[str], optional): Text of the notification. Defaults to None.
            show_alert (Optional[bool], optional): If True, an alert will be shown by the client instead of a notification. Defaults to None.
            url (Optional[str], optional): URL that will be opened by the user's client. Defaults to None.
            cache_time (Optional[int], optional): The maximum amount of time in seconds that the result of the callback query may be cached client-side. Defaults to None.

        Returns:
            dict: On success, True is returned.
        """
        data = {
            'callback_query_id': callback_query_id,
            'text': text,
            'show_alert': show_alert,
            'url': url,
            'cache_time': cache_time
        }
        return await self.api.execute('answerCallbackQuery', data=data)
