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

from .chatMemberAdministrator import ChatMemberAdministrator
from .chatMemberBanned import ChatMemberBanned
from .chatMemberLeft import ChatMemberLeft
from .chatMembersMember import ChatMembersMember
from .chatMemberOwner import ChatMemberOwner
from .chatMemberRestricted import ChatMemberRestricted


class ChatMember(
    ChatMemberAdministrator,
    ChatMemberBanned,
    ChatMemberLeft,
    ChatMembersMember,
    ChatMemberOwner,
    ChatMemberRestricted,
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
