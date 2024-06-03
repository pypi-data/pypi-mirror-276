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

from typing import Callable

import grambot

from grambot.filters import Filters
from grambot.handlers import MessageHandler

class OnMessage:
    def onMessage(self: "grambot.GramClient", filters: Filters = None, group: int = 0):
        def decorator(func: Callable):
            try:
                self.addHandler(MessageHandler(func, filters), group)
            except Exception as e:
                print(e)
        return decorator
