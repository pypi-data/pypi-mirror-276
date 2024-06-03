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

from typing import List, Union

import grambot

from grambot.types.chats import ChatMember


class GetChatAdministrators:
    async def getChatAdministrators(
        self: "grambot.GramClient",
        chatId: Union[int, str] = None
    ) -> List["ChatMember"]:
        self.chatId = chatId
        self.params: dict = {}
        if self.chatId:
            self.params["chat_id"] = self.chatId
        data = self.api._method("getChatAdministrators", self.params)
        return [ChatMember(**x) for x in data]