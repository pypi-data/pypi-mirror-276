from __future__ import annotations


import msgspec
import typing
import aiohttp
import pathlib
import urllib

class KiranResource(msgspec.Struct):
    """
    A base class defining the resource objects. This might 
    include all the file-like structures returned by API.
    This is meant to be subclassed into the package's 
    resource objects.
    """
    file_id : str
    """
    An identifier for this file defined by Telegram.
    """
    file_unique_id : str
    """
    A unique identifier for this file, which is supposed to be the same over time and for different bots.
    """
    file_name: typing.Optional[str]
    """
    Name of the file. Not guaranteed to be unique.
    """
    mime_type: typing.Optional[str]
    """
    MIME type of the file as defined by the invoker.
    """
    file_size : typing.Optional[int]
    """
    The size of file in bytes.
    """
    file_path: typing.Optional[str]
    """
    A relative path to the file.
    """
    def __init__(self, *args: tuple[str, ...], **kwargs: typing.Dict[str, typing.Any]):
        super().__init__(*args, **kwargs)

"""    async def download(self, path: typing.Union[str, pathlib.Path]) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get() as resp:
                with open(path, "wb") as f:
                    f.write(await resp.read())
"""