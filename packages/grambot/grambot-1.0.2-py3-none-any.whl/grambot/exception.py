# ===========================================================
#             Copyright (C) 2023-present AyiinXd
# ===========================================================
# ||                                                       ||
# ||              _         _ _      __  __   _            ||
# ||             / \  _   _(_|_)_ __ \ \/ /__| |           ||
# ||            / _ \| | | | | | '_ \ \  // _` |           ||
# ||           / ___ \ |_| | | | | | |/  \ (_| |           ||
# ||          /_/   \_\__, |_|_|_| |_/_/\_\__,_|           ||
# ||                  |___/                                ||
# ||                                                       ||
# ===========================================================
#  Appreciating the work of others is not detrimental to you
# ===========================================================

from typing import Tuple


class GrambotError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class CacheException(GrambotError):
    def __init__(self, message: str):
        super().__init__(message)


class InitializationException(GrambotError):
    def __init__(self, message: str):
        super().__init__(message)

class TimedOut(GrambotError):
    def __init__(self, message: str):
        super().__init__("TimeOut Error: {}".format(message))

class FloodWait(GrambotError):
    def __init__(self, retry_after: int):
        super().__init__(f"Floodwait exceeded. Retry in {retry_after} seconds")
        self.retry_after: int = retry_after

    def __reduce__(self) -> Tuple[type, Tuple[float]]:  # type: ignore[override]
        return self.__class__, (self.retry_after,)