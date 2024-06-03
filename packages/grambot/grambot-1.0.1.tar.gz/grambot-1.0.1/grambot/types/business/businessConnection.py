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


class BusinessConnection:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.user = kwargs.get("user", None)
        self.userChatId = kwargs.get("user_chat_id", None)
        self.date = kwargs.get("date", None)
        self.canReply = kwargs.get("can_reply", None)
        self.isEnabled = kwargs.get("is_enabled", None)

    @classmethod
    def parseBusinessConnection(cls, businessConnection: object):
        return BusinessConnection(
            id=businessConnection.get("id"),
            user=businessConnection.get("user"),
            userChatId=businessConnection.get("user_chat_id"),
            date=businessConnection.get("date"),
            canReply=businessConnection.get("can_reply"),
            isEnabled=businessConnection.get("is_enabled"),
        )
