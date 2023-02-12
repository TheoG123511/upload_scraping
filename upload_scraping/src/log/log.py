#!/usr/bin/python3
# -*- coding: utf8 -*-
try:
    import os
    import logging
    from upload_scraping.src.config import Config
    from upload_scraping.src.utils.singleton import Singleton
    from upload_scraping.src.exceptions import LogWriteError
    # from upload_scraping.src.utils.colors import Colors
    from logging.handlers import RotatingFileHandler
    from io import StringIO
except ImportError:
    raise ImportError


class Logging(metaclass=Singleton):

    _TEST_MODE: bool = bool(os.environ.get("DEBUG", 0))
    _WRITE_MODE: str = "a"

    def __init__(self, format_log: str = '%(asctime)s :: %(levelname)s :: %(message)s',
                 level: str = logging.DEBUG) -> None:
        # initialize file log
        self._initialize_file()
        # Initial construct.
        self._format: str = format_log
        self._level: str = level
        self._logger = logging.getLogger()
        self._logger.setLevel(self._level)
        self._formatter = logging.Formatter(self._format)
        self._file_handler = RotatingFileHandler(Config.LOG_FILE_PATH, self._WRITE_MODE)
        self._file_handler.setLevel(logging.INFO)
        self._file_handler.setFormatter(self._formatter)
        self._logger.addHandler(self._file_handler)
        self._stream_handler = logging.StreamHandler()
        if self._TEST_MODE:
            self.debug_stream = StringIO()
            self.debug_handler = logging.StreamHandler(self.debug_stream)
            self._stream_handler.setLevel(logging.DEBUG)
            self._logger.addHandler(self._stream_handler)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    @staticmethod
    def display_color() -> None:
        if os.name == "nt":
            os.system("color B")

    @staticmethod
    def _initialize_file() -> None or Exception:
        if os.path.exists(Config.LOG_FILE_PATH):
            try:
                with open(Config.LOG_FILE_PATH, Logging._WRITE_MODE):
                    pass
            except (FileNotFoundError, OSError, PermissionError) as err:
                raise Exception("Unable to create log file %s" % err)
        # Logging.display_color()

    @property
    def text(self) -> str:
        if not self._TEST_MODE:
            return ""
        buff = self.debug_stream.tell()
        self.debug_stream.seek(0)
        _text = self.debug_stream.read().strip()
        self.debug_stream.seek(buff)
        return _text

    def write_log(self, class_name: object, message: str, level: str = "INFO") -> None:
        try:
            class_name = class_name.__class__.__name__
            # print(f"{Colors.OKCYAN}[{class_name}] {message}")
            print(f"[{class_name}] {message}")
            if level == "INFO":
                self._logger.info("[%s] %s" % (class_name, message))
            elif level == "DEBUG":
                self._logger.debug("[%s] %s" % (class_name, message))
            elif level == "WARNING":
                self._logger.warning("[%s] %s" % (class_name, message))
            elif level == "ERROR":
                self._logger.error("[%s] %s" % (class_name, message))
            elif level == "CRITICAL":
                self._logger.critical("[%s] %s" % (class_name, message))
            else:
                self._logger.warning(
                    "[%s][%s] Error, unknown level : %s" % (self.__class__.__name__, class_name, level)
                )
        except TypeError as _err:
            raise LogWriteError("[%s][%s] Error -> %s" % (self.__class__.__name__, class_name, _err))
