import typing
import pathlib
import datetime
import aiofiles
import pathlib

class LoggerSettings:
    """
    Logger settings, this has to be setup by the user for internal logging in Kiran.
    This would be able to log everything that are generated as `Exceptions` in Kiran.
    
    Parameters
    ----------
    level : typing.Literal["debug", "basic", "no-log"]
        Logging level, default is basic
    log_file : typing.Optional[typing.Union[str, pathlib.Path]]
        Logging file, default is None
    clean_logs : typing.Optional[bool]
        Weather to use clean logging, default is True. This would use the system level module to display logs.
    """
    def __init__(
        self, 
        level : typing.Literal["debug", "basic", "no-log"] = "basic", 
        log_file : typing.Optional[typing.Union[str, pathlib.Path]] = None,
        clean_logs: typing.Optional[bool]=True,
        enable_colors: typing.Optional[bool]=True
    ) -> None:
        self.level = level
        self.log_file = log_file
        self.clean_logs = clean_logs
        self.enable_colors = enable_colors
    

class Logger:
    def __init__(self, settings: typing.Optional[LoggerSettings]) -> None:
        if settings:
            self.log_settings = settings
            if self.log_settings.log_file is not None:
                if isinstance(self.log_settings.log_file, str):
                    self.log_file = pathlib.Path(self.log_settings.log_file)
                if isinstance(self.log_settings.log_file, pathlib.Path):
                    self.log_file = self.log_settings.log_file
                else:
                    raise ValueError("Invalid log file type.")
                self.file_session = aiofiles.open(self.log_file, mode="a")
        else: 
            raise ValueError("No logger settings provided")
    