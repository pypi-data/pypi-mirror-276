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


class ChatMemberRestricted:
    def __init__(self, **kwargs):
        self.status = kwargs.get("status", None)
        self.user = User(**kwargs.get("user", {}))
        self.isMember = kwargs.get("is_member", None)
        self.canSendMessages = kwargs.get("can_send_messages", None)
        self.canSendAudios = kwargs.get("can_send_audios", None)
        self.canSendDocuments = kwargs.get("can_send_documents", None)
        self.canSendPhotos = kwargs.get("can_send_photos", None)
        self.canSendVideos = kwargs.get("can_send_videos", None)
        self.canSendVideoNotes = kwargs.get("can_send_video_notes", None)
        self.canSendVoiceNotes = kwargs.get("can_send_voice_notes", None)
        self.canSendPolls = kwargs.get("can_send_polls", None)
        self.canSendOtherMessages = kwargs.get("can_send_other_messages", None)
        self.canAddWebPagePreviews = kwargs.get("can_add_web_page_previews", None)
        self.canChangeInfo = kwargs.get("can_change_info", None)
        self.canInviteUsers = kwargs.get("can_invite_users", None)
        self.canPinMessages = kwargs.get("can_pin_messages", None)
        self.canManageTopics = kwargs.get("can_manage_topics", None)
        self.untilDate = kwargs.get("until_date", None)
    
    def parseChatMemberRestricted(self, chatMemberRestricted: object):
        self.chatMemberRestricted = chatMemberRestricted
        try:
            return self.chatMemberRestricted.__dict__
        except AttributeError:
            return self.chatMemberRestricted