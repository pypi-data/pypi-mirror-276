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



class CallbackQuery:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.fromUser = kwargs.get("from", None)
        self.message = kwargs.get("message", None)
        self.inlineMessageId = kwargs.get("inline_message_id", None)
        self.chatInstance = kwargs.get("chat_instance", None)
        self.data = kwargs.get("data", None)
        self.gameShortName = kwargs.get("game_short_name", None)

    def parseCallbackQuery(self, callbackQuery: object):
        self.callbackQuery = callbackQuery
        try:
            return self.callbackQuery.__dict__
        except AttributeError:
            return self.callbackQuery
