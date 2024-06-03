import io
import mimetypes
import re
import os
import aiofiles
import aiohttp
import inspect
import asyncio
import pybalebot
from pathlib import Path
from io import BytesIO
from .errors import RPCError
from .filters import Filter
from .types import Results, Message, CallbackQuery

def sanitize_filename(filename):
    # تعریف کاراکترهای غیرمجاز در ویندوز
    invalid_chars = r'[<>:"/\\|?*]'
    # جایگزینی کاراکترهای غیرمجاز با _
    return re.sub(invalid_chars, '_', filename)

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

    async def execute(self, name: str, data: dict = None, form = None):
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
            try:
                async with self.session.post(path, json=data, data=form) as response:
                    response_data = await response.json()
                    if response_data.get('ok'):
                        response_data.pop('ok')
                        return Results(response_data)
                    error_code = response_data.get('error_code')
                    description = response_data.get('description')
                    raise RPCError(description, code=error_code)

            except Exception as e:
                pass

    async def process_update(self, update: Results):
        """
        Process an update from the API.

        :param update: The update data.
        """
        event_type = self.determine_event_type(update)
        if event_type == 'message':
            update_message = Message(update.find_keys(event_type).original_update)
        elif event_type == 'callback_query':
            update_message = CallbackQuery(update.find_keys(event_type).original_update)
        else:
            update_message = Message(update.find_keys(event_type).original_update)

        update_message.__setattr__('client', self.client)

        if event_type in self.client.handlers:
            for handler_name, handler_info in self.client.handlers[event_type].items():
                handler = handler_info['handler']
                filters = handler_info['filters']

                filter_results = []
                for filter_group in filters:
                    for filter_func in filter_group:
                        #try:
                            if isinstance(filter_func, Filter):
                                result = await filter_func(self.client, update_message)
                            else:
                                result = await filter_func(self.client, update_message) if inspect.iscoroutinefunction(filter_func) else filter_func(self.client, update_message)
                            filter_results.append(result)
                        # except Exception as e:
                        #     print(f"Error in filter function {filter_func}: {e}")
                        #     filter_results.append(False)

                if all(filter_results):
                    #try:
                        await handler(self.client, update_message)
                    # except Exception as e:
                    #     print(f"Error in handler {handler_name}: {e}")

    async def get_updates(self):
        """
        Continuously fetch updates from the Bale API and process them.
        """
        await self.client.delete_webhook()

        while True:
            try:
                updates = await self.client.get_updates(offset=self.offset, limit=1)
                updates_result = updates.result

                if updates_result:
                    update = updates_result[-1]
                    self.offset = update.update_id + 1
                    asyncio.create_task(self.process_update(update=update))

            except Exception:
                await asyncio.sleep(1)
                #print('Error in getting updates from Bale:', e)

    def determine_event_type(self, update: Results) -> str:
        if update.edited_message:
            return 'edited_message'
        elif update.callback_query:
            return 'callback_query'
        elif update.inline_query:
            return 'inline_query'
        elif update.chosen_inline_result:
            return 'chosen_inline_result'
        elif update.chat_member_updated:
            return 'chat_member_updated'
        elif update.chat_join_request:
            return 'chat_join_request'
        elif update.deleted_messages:
            return 'deleted_messages'
        elif update.user_status:
            return 'user_status'
        elif update.poll:
            return 'poll'
        elif update.disconnect:
            return 'disconnect'
        elif update.message:
            return 'message'
        else:
            return 'raw_update'

    async def download_file(self, file_id: str, file_name: str=None, in_memory: bool=False, block: bool=True, progress=None, progress_args=(), save: bool=False):
        get_file = await self.client.get_file(file_id=file_id)
        file_path = get_file.result.file_path

        async with self.session.get(f'/file/bot{self.client.bot_token}/{file_path}') as response:
            if response.ok:
                mime_type = response.headers.get('Content-Type', '')
                extension = mimetypes.guess_extension(mime_type) or '.bin'

                if file_name is None:
                    file_name = file_path.split('/')[-1]

                # تنظیم اسم فایل
                file_name = sanitize_filename(file_name) + extension

                # بررسی و ایجاد پوشه downloads در صورت نیاز
                if save:
                    download_folder = 'downloads'
                    os.makedirs(download_folder, exist_ok=True)
                    file_name = os.path.join(download_folder, file_name)

                if not save and not in_memory:
                    # بررسی وجود پوشه و ساخت آن
                    if file_name.endswith('/'):
                        os.makedirs(file_name, exist_ok=True)
                        file_name = os.path.join(file_name, sanitize_filename(file_path.split('/')[-1]) + extension)
                    else:
                        directory = os.path.dirname(file_name)
                        if directory:
                            os.makedirs(directory, exist_ok=True)

                total_size = int(response.headers.get('Content-Length', 0))
                current_size = 0

                if not save and in_memory:
                    data = await response.read()
                    file_like_object = io.BytesIO(data)
                    file_like_object.name = file_name
                    return file_like_object

                async with aiofiles.open(file_name, 'wb') as f:
                    async for chunk in response.content.iter_chunked(1024):
                        await f.write(chunk)
                        current_size += len(chunk)
                        if progress:
                            progress(current_size, total_size, *progress_args)

                if not in_memory:
                    return os.path.abspath(file_name)
                else:
                    with open(file_name, 'rb') as f:
                        file_like_object = io.BytesIO(f.read())
                        file_like_object.name = file_name
                        return file_like_object
            else:
                raise ValueError(f"Failed to download file: {response.status}")