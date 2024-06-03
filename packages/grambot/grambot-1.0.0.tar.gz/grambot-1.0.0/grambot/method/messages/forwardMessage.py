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
from grambot.types.messages.message import Message


class ForwardMessage:
    def forwardMessage(
        self: "grambot.GramClient",
        chatId: Union[int, str] = None,
        fromChatId: Union[int, str] = None,
        messageId: int = None,
        messageThreadId: int = None,
        disableNotification: bool = None,
        protectContent: bool = None,
    ) -> "Message":
        self.chatId = chatId
        self.messageThreadId = messageThreadId
        self.fromChatId = fromChatId
        self.disableNotification = disableNotification
        self.protectContent = protectContent
        self.messageId = messageId
        self.params: dict = {}
        if self.chatId:
            self.params["chat_id"] = self.chatId
        if self.fromChatId:
            self.params["from_chat_id"] = self.fromChatId
        if self.messageId:
            self.params["message_id"] = self.messageId
        if self.messageThreadId:
            self.params["message_thread_id"] = self.messageThreadId
        if self.disableNotification:
            self.params["disable_notification"] = self.disableNotification
        if self.protectContent:
            self.params["protect_content"] = self.protectContent
        data = self.api._method("forwardMessage", self.params)
        return Message(**data)