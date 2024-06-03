import asyncio
from .api import BaleAPI
from .methods import Methods

class Client(Methods):
    def __init__(self, name: str, max_retry: int = 3, bot_token: str = None, base_url: str = None) -> None:
        """
        Initialize the Client instance.

        :param name: The name of the bot.
        :param bot_token: The bot token for authentication.
        :param base_url: The base URL for the Bale API.
        """
        super().__init__()
        self.bot_token = bot_token
        self.base_url = base_url
        self.max_retry = int(max_retry)
        self.name = name
        self.handlers = {
            'message': {},
            'edited_message': {},
            'callback_query': {},
            'inline_query': {},
            'chosen_inline_result': {},
            'chat_member_updated': {},
            'chat_join_request': {},
            'deleted_messages': {},
            'user_status': {},
            'poll': {},
            'disconnect': {},
            'raw_update': {}
        }
        self.api = None

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, *args, **kwargs):
        return await self.stop()

    async def start(self):
        """
        Start the client by connecting to the Bale API.
        """
        if self.api is None:
            await self.connect()

    async def connect(self):
        """
        Connect to the Bale API and retrieve bot information.
        """
        if self.bot_token is None:
            self.bot_token = input('Please enter your bot token: ')

        self.api = BaleAPI(client=self)
        self.me = await self.get_me()
        print(f'connect to the Bale API with {self.me.username} bot\n')

    async def stop(self):
        """
        Stop the client by closing the Bale API session.
        """
        await self.api.close()

    def run(self):
        """
        Run the client to start receiving updates.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.start())
        loop.run_until_complete(self.api.get_updates())

    def on_message(self, *filters):
        def decorator(func):
            self.add_handler('message', func, filters)
            return func
        return decorator

    def on_edited_message(self, *filters):
        def decorator(func):
            self.add_handler('edited_message', func, filters)
            return func
        return decorator

    def on_callback_query(self, *filters):
        def decorator(func):
            self.add_handler('callback_query', func, filters)
            return func
        return decorator

    def on_inline_query(self, *filters):
        def decorator(func):
            self.add_handler('inline_query', func, filters)
            return func
        return decorator

    def on_chosen_inline_result(self, *filters):
        def decorator(func):
            self.add_handler('chosen_inline_result', func, filters)
            return func
        return decorator

    def on_chat_member_updated(self, *filters):
        def decorator(func):
            self.add_handler('chat_member_updated', func, filters)
            return func
        return decorator

    def on_chat_join_request(self, *filters):
        def decorator(func):
            self.add_handler('chat_join_request', func, filters)
            return func
        return decorator

    def on_deleted_messages(self, *filters):
        def decorator(func):
            self.add_handler('deleted_messages', func, filters)
            return func
        return decorator

    def on_user_status(self, *filters):
        def decorator(func):
            self.add_handler('user_status', func, filters)
            return func
        return decorator

    def on_poll(self, *filters):
        def decorator(func):
            self.add_handler('poll', func, filters)
            return func
        return decorator

    def on_disconnect(self, *filters):
        def decorator(func):
            self.add_handler('disconnect', func, filters)
            return func
        return decorator

    def on_raw_update(self, *filters):
        def decorator(func):
            self.add_handler('raw_update', func, filters)
            return func
        return decorator

    def add_handler(self, event_type, func, *filters):
        self.handlers[event_type][func.__name__] = {'handler': func, 'filters': filters}