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

from ...users import User


class ChatMemberAdministrator:
    def __init__(self, **kwargs):
        self.status = kwargs.get("status", None)
        self.user = User(kwargs.get("user", {}))
        self.canBeEdited = kwargs.get("can_be_edited", None)
        self.isAnonymous = kwargs.get("is_anonymous", None)
        self.canManageChat = kwargs.get("can_manage_chat", None)
        self.canDeleteMessages = kwargs.get("can_delete_messages", None)
        self.canManageVideoChats = kwargs.get("can_manage_video_chats", None)
        self.canRestrictMembers = kwargs.get("can_restrict_members", None)
        self.canPromoteMembers = kwargs.get("can_promote_members", None)
        self.canChangeInfo = kwargs.get("can_change_info", None)
        self.canInviteUsers =	kwargs.get("can_invite_users", None)
        self.canPostUtories =	kwargs.get("can_post_stories", None)
        self.canEditStories = kwargs.get("can_edit_stories", None)
        self.canDeleteStories = kwargs.get("can_delete_stories", None)
        self.canEditMessages = kwargs.get("can_edit_messages", None)
        self.canPinMessages = kwargs.get("can_pin_messages", None)
        self.canManageTopics = kwargs.get("can_manage_topics", None)
        self.customTitle = kwargs.get("custom_title", None)
    
    def parseChatAdministrator(self, chatAdministrator: object):
        self.chatAdministrator = chatAdministrator
        try:
            self.chatAdministrator.__dict__
        except AttributeError:
            return self.chatAdministrator