import typing
import asyncio
import webbrowser
import sys

from kiran.impl import KiranBot

if typing.TYPE_CHECKING:
    from .impl import KiranBot


class KiranBaseException(Exception):
    def __init__(self, message: str, client: typing.Optional["KiranBot"] = None, *args: object) -> None:
        self.client = client
        self.message = message
        super().__init__(*args)
        
class KiranTypeError(KiranBaseException):
    ...
    
class KiranValueError(KiranBaseException):
    ...

class KiranKeyError(KiranBaseException):
    ...

class KiranRuntimeError(KiranBaseException):
    def __init__(self,event_loop: asyncio.BaseEventLoop, message: str, client: typing.Optional["KiranBot"] = None, *args: object) -> None:
        self.event_loop = event_loop
        super().__init__(message, client, *args)


class KiranUnkownError(KiranBaseException):
    def __init__(self, message: str, client: typing.Optional["KiranBot"] = None, *args: object) -> None:
        super().__init__(message, client, *args)
    
    def bug_drop(self) -> None:
        try:
            webbrowser.open_new_tab("https://github.com/halfstackpgr/kiran/issues/new")
        except Exception:
            sys.stdout.write("\nKindly submit a report along with the traceback to https://https://github.com/halfstackpgr/kiran/issues/new\n")