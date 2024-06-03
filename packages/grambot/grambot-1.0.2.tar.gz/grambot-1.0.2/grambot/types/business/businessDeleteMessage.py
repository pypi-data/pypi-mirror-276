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


class BusinessDeleteMessage:
    def __init__(self, **kwargs):
        self.businessConnectionId = kwargs.get("business_connection_id", None)
        self.chat = kwargs.get("chat", None)
        self.messageIds = kwargs.get("message_ids", None)
    
    def parseBusinessDeleteMessage(self, businessDeleteMessage: object):
        self.businessDeleteMessage = businessDeleteMessage
        try:
            return self.businessDeleteMessage.__dict__
        except AttributeError:
            return self.businessDeleteMessage