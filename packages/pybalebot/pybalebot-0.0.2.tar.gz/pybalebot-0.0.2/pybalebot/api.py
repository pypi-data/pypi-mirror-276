import aiohttp
import inspect
import asyncio
import pybalebot
from .errors import RPCError
from .filters import Filter
from .types import Results, Message

class BaleAPI:
    BASE_URL = 'https://tapi.bale.ai'

    def __init__(self, client=None) -> None:
        """
        Initialize the BaleAPI instance.
        
        :param client: The client instance which contains bot_token and other configurations.
        """
        self.client: "pybalebot.Client" = client
        self.offset = 0
        self.session = aiohttp.ClientSession(
            base_url=client.base_url or self.BASE_URL,
            connector=aiohttp.TCPConnector(),
            timeout=aiohttp.ClientTimeout(total=20)
        )

    async def close(self):
        """
        Close the aiohttp session.
        """
        await self.session.close()

    async def execute(self, name: str, data: dict = None, update: bool = False):
        """
        Execute a command on the Bale API.

        :param name: The API method name.
        :param data: The data to be sent with the request.
        :param update: Whether the request is an update.
        :return: Results object if the request is successful.
        :raises: RPCError if the request fails.
        """
        path = f'/bot{self.client.bot_token}/{name}'
        for _ in range(self.client.max_retry):
            async with self.session.post(path, json=data) as response:
                response_data = await response.json()
                if response_data.get('ok'):
                    response_data.pop('ok')
                    return Results(response_data)
                error_code = response_data.get('error_code')
                description = response_data.get('description')
                raise RPCError(description, code=error_code)

    async def process_update(self, update: Results):
        """
        Process an update from the Bale API.

        :param update: The update data.
        """
        update_message = Message(update.original_update)
        update_message.client = self.client

        for handler, filters in self.client.handlers.copy().items():
            filter_results = []
            for filter_func in filters:
                try:
                    if isinstance(filter_func, Filter):
                        result = await filter_func(self.client, update_message)
                    else:
                        result = await filter_func(self.client, update_message) if inspect.iscoroutinefunction(filter_func) else filter_func(self.client, update_message)
                    filter_results.append(result)
                except Exception as e:
                    # Debugging: Print the filter_func and error message
                    print(f"Error in filter function {filter_func}: {e}")
                    filter_results.append(False)

            if all(filter_results):
                try:
                    # Ensure handler is not None
                    if handler is None:
                        raise TypeError("Handler is None")
                    
                    # Call the handler
                    await handler(self.client, update_message)
                except Exception as e:
                    # Debugging: Print the handler and error message
                    print(f"Error in handler {handler}: {e}")

    async def get_updates(self):
        """
        Continuously fetch updates from the Bale API and process them.
        """
        await self.client.set_webhook()
        while True:
            try:
                updates = await self.client.get_updates(offset=self.offset)
                updates_result = updates.result

                if updates_result:
                    self.offset = updates_result[-1].update_id + 1

                for update in updates_result:
                    asyncio.create_task(self.process_update(update=update))
            except Exception as e:
                await asyncio.sleep(3)
                print('Error in getting updates from Bale:', e)
