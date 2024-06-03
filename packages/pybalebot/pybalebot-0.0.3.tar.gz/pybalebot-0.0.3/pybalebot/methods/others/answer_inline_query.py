from pybalebot.types import InlineQueryResult
from typing import List, Optional
import pybalebot

class AnswerInlineQuery:
    async def answer_inline_query(
            self: "pybalebot.Client",
            inline_query_id: str,
            results: List[InlineQueryResult],
            cache_time: Optional[int] = None,
            is_personal: Optional[bool] = None,
            next_offset: Optional[str] = None,
            switch_pm_text: Optional[str] = None,
            switch_pm_parameter: Optional[str] = None
    ) -> dict:
        """Send a response to an inline query.

        Args:
            inline_query_id (str): Unique identifier for the answered query.
            results (List[InlineQueryResult]): A list of results for the inline query.
            cache_time (Optional[int], optional): The maximum amount of time in seconds that the result of the inline query may be cached on the server. Defaults to None.
            is_personal (Optional[bool], optional): Pass True if results may be cached on the server side only for the user that sent the query. Defaults to None.
            next_offset (Optional[str], optional): Pass the offset that a client should send in the next query with the same text to receive more results. Defaults to None.
            switch_pm_text (Optional[str], optional): If passed, clients will display a button with specified text that switches the user to a private chat with the bot. Defaults to None.
            switch_pm_parameter (Optional[str], optional): Parameter for the start message sent to the bot when user presses the switch button. Defaults to None.

        Returns:
            dict: On success, True is returned.
        """
        data = {
            'inline_query_id': inline_query_id,
            'results': [result.to_dict() for result in results],
            'cache_time': cache_time,
            'is_personal': is_personal,
            'next_offset': next_offset,
            'switch_pm_text': switch_pm_text,
            'switch_pm_parameter': switch_pm_parameter
        }
        return await self.api.execute('answerInlineQuery', data=data)
