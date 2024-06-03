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

import asyncio
import logging

import grambot
from grambot.exception import GrambotError


logs = logging.getLogger("grambot")


class Start:
    async def _start(self: "grambot.GramClient", ready: asyncio.Event = None):
        if not self._initialize:
            self._initialize = True
            print("\nGramBot - Copyright (C) 2024 - AyiinXd\n")
        self.running = True
        self.me = await self.getMe()
