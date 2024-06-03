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
import inspect
import logging
import signal
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from signal import signal as signal_fn, SIGINT, SIGTERM, SIGABRT
from typing import Optional, Tuple

from .apiClient import ApiClient
from .cache import Cache
from .exception import GrambotError
from .method import Method
from .types import User, Update
from .session import Session


logs = logging.getLogger("grambot")

# Signal number to name
signals = {
    k: v for v, k in signal.__dict__.items()
    if v.startswith("SIG") and not v.startswith("SIG_")
}

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
        self.offset = -1
        self.parse_mode = parse_mode
        self.api = ApiClient(self.token)
        self._initialize = False
        self.cache = Cache(self.name)
        self.session = Session(client=self, name=self.name)
        self.handlers: list = []
        self.sessionName: str = None
        self.executor = ThreadPoolExecutor()

        if self.parse_mode:
            if self.parse_mode not in ["html", "markdown", "markdownv2"]:
                raise GrambotError("Parse mode must be html, markdown or markdownv2")

        self.me: Optional[User] = None
        self.loop = asyncio.get_event_loop()

        self.is_running = False
        self.groups = OrderedDict()

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
        self.offset = offset or -1
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
        return [Update(**d) for d in data]

    async def handleWorkers(self):
        while self._initialize:
            updates = await self.getUpdates(offset=-1 + 1)
            for update in updates:
                if update is None:
                    break
                self.offset = update.updateId
                try:
                    updated = self._parseUpdates(update)

                    for group in self.groups.values():
                        for handler in group:
                            check = await handler.check(self, updated)
                            
                            if check:
                                if inspect.iscoroutinefunction(handler.callback):
                                    await handler.callback(self, updated)
                                else:
                                    self.loop.run_in_executor(
                                        self.executor,
                                        handler.callback,
                                        self,
                                        updated
                                    )
                                break
                except Exception as exe:
                    logging.error(exe, exc_info=True)
                    continue

    async def idle(self):
        def signal_handler(signum, __):
            logs.info(f"Stop signal received ({signals[signum]}). Exiting...")
            self.is_idling = False

        for s in (SIGINT, SIGTERM, SIGABRT):
            signal_fn(s, signal_handler)

        self.is_idling = True
        logs.info('[Bot] Started Bot session. Idling....')

        while self.is_idling:
            await asyncio.sleep(1)

    async def stop(self):
        self.session.delete_instance()
        self._initialize = False
        self.groups.clear()

    def addHandler(self, handler, group: int):
        try:
            if group not in self.groups:
                self.groups[group] = []
                self.groups = OrderedDict(sorted(self.groups.items()))

            self.groups[group].append(handler)
        finally:
            pass

    @staticmethod
    def _parseUpdates(update: Update):
        if update.inlineQuery:
            updated = update.inlineQuery
        elif update.callbackQuery:
            updated = update.callbackQuery
        elif (update.message or update.editedMessage or update.channelPost
        or update.editedChannelPost):
            updated = update.message
        else:
            updated = update

        return updated
