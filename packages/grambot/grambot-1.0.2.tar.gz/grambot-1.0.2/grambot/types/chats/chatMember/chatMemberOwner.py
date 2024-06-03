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


class ChatMemberOwner:
    def __init__(self, **kwargs):
        self.status = kwargs.get("status", None)
        self.user = kwargs.get("user", None)
        self.isAnonymous = kwargs.get("is_anonymous", None)
        self.customTitle = kwargs.get("custom_title", None)
    
    def parseChatMemberOwner(self, owner: object):
        self.owner = owner
        try:
            return self.owner.__dict__
        except AttributeError:
            return self.owner