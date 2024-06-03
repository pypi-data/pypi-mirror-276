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


from .users import User


class InlineQuery:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.fromUser: User = kwargs.get("from", None)
        self.query = kwargs.get("query", None)
        self.offset = kwargs.get("offset", None)
        self.chat_type = kwargs.get("chat_type", None)
        self.location = kwargs.get("location", None)
    
    def parseInlineQuery(self, iq: object):
        self.iq = iq
        try:
            return self.iq.__dict__
        except AttributeError:
            return self.iq
