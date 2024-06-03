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
from grambot.types import Message


class SendMessage:
    async def sendMessage(
        self: "grambot.GramClient",
        chatId: Union[int, str] = None,
        text: str = None,
        *,
        parse_mode: str = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        entities: any = None,
        link_preview: bool = None,
        protect_content: bool = None,
    ) -> "Message":
        self.chatId = chatId
        self.text = text
        self.parse_mode = parse_mode or self.parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.disableNotification = disable_notification
        self.reply_to_message_id = reply_to_message_id
        self.entities = entities
        self.link_preview = link_preview
        self.protectContent = protect_content
        # self.reply_markup = reply_markup
        self.params: dict = {}
        if self.chatId:
            self.params["chat_id"] = self.chatId
        if self.text:
            self.params["text"] = self.text
        if self.parse_mode:
            self.params["parse_mode"] = self.parse_mode
        if self.disable_web_page_preview:
            self.params["disable_web_page_preview"] = self.disable_web_page_preview
        if self.disableNotification:
            self.params["disable_notification"] = self.disableNotification
        if self.reply_to_message_id:
            self.params["reply_to_message_id"] = self.reply_to_message_id
        if self.entities:
            self.params["entities"] = self.entities
        if self.link_preview:
            self.params["link_preview_options"] = self.link_preview
        if self.protectContent:
            self.params["protect_content"] = self.protectContent
        data = self.api._method("sendMessage", params=self.params)
        return Message(**data)
    
    
    def editMessageText(
        self: "grambot.GramClient",
        chatId: Union[int, str] = None,
        message_id: int = None,
        text: str = None,
        parse_mode: str = None,
        disable_web_page_preview: bool = None,
        entities: any = None,
        reply_markup: any = None,
    ) -> "grambot.types.message.Message":
        self.chatId = chatId
        self.message_id = message_id
        self.text = text
        self.parse_mode = parse_mode or self.parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.entities = entities
        self.reply_markup = reply_markup
        self.params: dict = {}
        if self.chatId:
            self.params["chat_id"] = self.chatId