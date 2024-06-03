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

from typing import List

from .business import BusinessConnection, BusinessDeleteMessage
from .messages import Message


class Update:
    def __init__(self, **kwargs):
        self.updateId = kwargs.get("update_id", None)
        self.message = kwargs.get("message", None)
        self.editedMessage = kwargs.get("edited_message", None)
        self.channelPost = kwargs.get("channel_post", None)
        self.editedChannelPost = kwargs.get("edited_channel_post", None)
        self.businessConnection = kwargs.get("business_connection", None)
        self.businessMessage = kwargs.get("business_message", None)
        self.editedBusinessMessage = kwargs.get("edited_business_message", None)
        self.deletedBusinessMessages = kwargs.get("deleted_business_messages", None)
        self.messageReaction = kwargs.get("message_reaction", None)
        self.messageReactionCount = kwargs.get("message_reaction_count", None)
        self.inlineQuery = kwargs.get("inline_query", None)
        self.chosenInlineResult = kwargs.get("chosen_inline_result", None)
        self.callbackQuery = kwargs.get("callback_query", None)
        self.shippingQuery = kwargs.get("shipping_query", None)
        self.preCheckoutQuery = kwargs.get("pre_checkout_query", None)
        self.poll = kwargs.get("poll", None)
        self.pollAnswer = kwargs.get("poll_answer", None)
        self.myChatMember = kwargs.get("my_chat_member", None)
        self.chatMember = kwargs.get("chat_member", None)
        self.chatJoinRequest = kwargs.get("chat_join_request", None)
        self.chatBoost = kwargs.get("chat_boost", None)
        self.removedChatBoost = kwargs.get("removed_chat_boost", None)
        self.arrayEmpty = []
    
    def parseUpdate(self, update: object):
        if update.get("message") is not None:
            self.message = Message().parseMessage(update.get("message"))
        if update.get("edited_message") is not None:
            self.editedMessage = Message().parseMessage(update.get("edited_message"))
        if update.get("channel_post") is not None:
            self.channelPost = Message().parseMessage(update.get("channel_post"))
        if update.get("edited_channel_post") is not None:
            self.editedChannelPost = Message().parseMessage(update.get("edited_channel_post"))
        if update.get("business_connection") is not None:
            self.businessConnection = BusinessConnection().parseBusinessConnection(update.get("business_connection"))
        if update.get("business_message") is not None:
            self.businessMessage = Message().parseMessage(update.get("business_message"))
        if update.get("edited_business_message") is not None:
            self.editedBusinessMessage = Message().parseMessage(update.get("edited_business_message"))
        if update.get("deleted_business_messages") is not None:
            self.deletedBusinessMessages = BusinessDeleteMessage().parseDeletedBusinessMessages(update.get("deleted_business_messages"))
        try:
            return update.__dict__
        except AttributeError:
            return update

    def arrayUpdate(self, updates: list) -> List["Update"]:
        if not updates:
            return []
        return [self.parseUpdate(update) for update in updates]