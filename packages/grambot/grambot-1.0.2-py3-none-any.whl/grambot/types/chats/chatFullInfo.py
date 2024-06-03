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


class ChatFullInfo:
    def __init__(self, **kwargs):
        self.id: int = kwargs.get("id", None)
        self.title: str = kwargs.get("title", None)
        self.type: str = kwargs.get("type", None)
        self.invite_link: str = kwargs.get("invite_link", None)
        self.permissions: dict = kwargs.get("permissions", None)
        self.join_to_send_messages: bool = kwargs.get("join_to_send_messages", None)
        self.photo: dict = kwargs.get("photo", None)
        self.pinned_message: dict = kwargs.get("pinned_message", None)
        self.max_reaction_count: int = kwargs.get("max_reaction_count", None)
        self.accent_color_id: int = kwargs.get("accent_color_id", None)
    
    def parseChat(self, chat: object):
        self.chat = chat
        try:
            return self.chat.__dict__
        except AttributeError:
            return self.chat