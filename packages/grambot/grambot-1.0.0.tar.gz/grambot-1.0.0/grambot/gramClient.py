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
from typing import Optional, Tuple

from .apiClient import ApiClient
from .cache import Cache
from .exception import GrambotError
from .method import Method
from .types import User, Update


logs = logging.getLogger("grambot")

# MarkdownV2: https://core.telegram.org/bots/api#markdownv2-style

class GramClient(Method):
    """GramClient

        Args:
            token (str): Token from @BotFather is required. Defaults to None.
            name (str, `optional`): You can set `name` for the memory. Defaults to AyiinXd.
            parse_mode (str, `optional`): You can set `parse_mode` to the message with "html", "markdown" or "markdownv2". Defaults to "html".

        Raises:
            GrambotError: Token is required
            GrambotError: Parse mode must be html, markdown or markdownv2
    """
    def __init__(
        self,
        name: str = "AyiinXd",
        token: str = None,
        parse_mode: str = "html",
    ):
        super().__init__()
        self.token = token
        self.name = name
        self.parse_mode = parse_mode
        self.api = ApiClient(self.token)
        self._initialize = False
        self.session = Cache(self.name)
        self.handlers: list = []

        if self.parse_mode:
            if self.parse_mode not in ["html", "markdown", "markdownv2"]:
                raise GrambotError("Parse mode must be html, markdown or markdownv2")

        self.me: Optional[User] = None
        self.loop = asyncio.get_event_loop()

    @property
    def nameSession(self):
        return self._session

    @nameSession.setter
    def nameSession(self, value):
        self._session = value

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    async def start(self):
        if not self.token:
            raise GrambotError("Token is required")
        await self._start(asyncio.Event())
        return self

    async def getUpdates(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        timeout: Optional[int] = None,
        allowed_updates: list = None
    ) -> Tuple[Update, ...]:
        self.offset = offset
        self.limit = limit
        self.timeout = timeout
        self.allowed_updates = allowed_updates
        self.params = {}
        if self.offset:
            self.params["offset"] = self.offset
        if self.limit:
            self.params["limit"] = self.limit
        if self.timeout:
            self.params["timeout"] = self.timeout
        if self.allowed_updates:
            self.params["allowed_updates"] = self.allowed_updates
        data = self.api._method("getUpdates", self.params)
        if not data:
            logs.info("No updates")
            return 
        else:
            logs.info("Get %s updates", len(data))
        return Update().arrayUpdate(data)
