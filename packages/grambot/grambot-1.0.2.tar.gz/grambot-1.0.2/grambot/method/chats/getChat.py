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

from typing import Union

import grambot
from grambot.types import ChatFullInfo


class GetChat:
    async def getChat(self: "grambot.GramClient", chatId: Union[int, str] = None) -> "ChatFullInfo":
        self.chatId = chatId
        self.params: dict = {}
        if self.chatId:
            self.params["chat_id"] = self.chatId
        data = self.api._method("getChat", self.params)
        return ChatFullInfo(**data)