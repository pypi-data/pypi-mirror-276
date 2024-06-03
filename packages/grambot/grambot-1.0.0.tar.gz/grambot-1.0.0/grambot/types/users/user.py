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


class User:
    def __init__(self, data):
        self.id = data.get("id", None)
        self.is_bot = data.get("is_bot", None)
        self.first_name = data.get("first_name", None)
        self.last_name = data.get("last_name", None)
        self.username = data.get("username", None)
        self.language_code = data.get("language_code", None)
        self.is_premium = data.get("is_premium", None)
        self.added_to_attachment_menu = data.get("added_to_attachment_menu", None)
        self.can_join_groups = data.get("can_join_groups", None)
        self.can_read_all_group_messages = data.get("can_read_all_group_messages", None)
        self.supports_inline_queries = data.get("supports_inline_queries", None)
        self.can_connect_to_business = data.get("can_connect_to_business", None)
    
    def parseUser(self, user: object):
        self._user = user
        return self._user.__dict__