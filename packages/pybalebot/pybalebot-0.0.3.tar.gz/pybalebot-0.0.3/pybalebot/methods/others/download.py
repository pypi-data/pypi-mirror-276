import pybalebot

class Download:
    async def download(
            self: "pybalebot.Client",
            file_id: str,
            file_name: str = None,
            in_memory: bool = False,
            progress = None,
            progress_args = (),
            save: bool = False
    ):
        return await self.api.download_file(
            file_id=file_id,
            file_name=file_name,
            in_memory=in_memory,
            progress=progress,
            progress_args=progress_args,
            save=save
        )