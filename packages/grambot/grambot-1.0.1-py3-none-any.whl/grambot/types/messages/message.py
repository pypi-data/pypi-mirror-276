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


class Message:
    def __init__(self, **kwargs):
        self.messageId: int = kwargs.get("message_id", None)
        self.messageThreadId = kwargs.get("message_thread_id", None)
        self.fromUser = kwargs.get("from", None)
        self.senderChat = kwargs.get("sender_chat", None)
        self.senderBoostCount = kwargs.get("sender_boost_count", None)
        self.senderBusinessBot = kwargs.get("sender_business_bot", None)
        self.date = kwargs.get("date", None)
        self.businessConnectionId = kwargs.get("business_connection_id", None)
        self.chat = kwargs.get("chat", None)
        self.forwardOrigin = kwargs.get("forward_origin", None)
        self.isTopicMessage = kwargs.get("is_topic_message", None)
        self.isAutomaticForward = kwargs.get("is_automatic_forward", None)
        self.replyToMessage = kwargs.get("reply_to_message", None)
        self.externalReply = kwargs.get("external_reply", None)
        self.quote = kwargs.get("quote", None)
        self.replyToStory = kwargs.get("reply_to_story", None)
        self.viaBot = kwargs.get("via_bot", None)
        self.editDate = kwargs.get("edit_date", None)
        self.hasProtectedContent = kwargs.get("has_protected_content", None)
        self.isFromOffline = kwargs.get("is_from_offline", None)
        self.mediaGroupId = kwargs.get("media_group_id", None)
        self.authorSignature = kwargs.get("author_signature", None)
        self.text = kwargs.get("text", None)
        self.entities = kwargs.get("entities", None)
        self.linkPreview = kwargs.get("link_preview_options", None)
        self.effectId = kwargs.get("effect_id", None)
        self.animation = kwargs.get("animation", None)
        self.audio = kwargs.get("audio", None)
        self.document = kwargs.get("document", None)
        self.photo = kwargs.get("photo", None)
        self.sticker = kwargs.get("sticker", None)
        self.story = kwargs.get("story", None)
        self.video = kwargs.get("video", None)
        self.videoNote = kwargs.get("video_note", None)
        self.voice = kwargs.get("voice", None)
        self.caption = kwargs.get("caption", None)
        self.captionEntities = kwargs.get("caption_entities", None)
        self.showCaptionAboveMedia = kwargs.get("show_caption_above_media", None)
        self.hasMediaSpoiler = kwargs.get("has_media_spoiler", None)
        self.contact = kwargs.get("contact", None)
        self.dice = kwargs.get("dice", None)
        self.game = kwargs.get("game", None)
        self.poll = kwargs.get("poll", None)
        self.venue = kwargs.get("venue", None)
        self.location = kwargs.get("location", None)
        self.newChatMembers = kwargs.get("new_chat_members", None)
        self.leftChatMember = kwargs.get("left_chat_member", None)
        self.newChatTitle = kwargs.get("new_chat_title", None)
        self.newChatPhoto = kwargs.get("new_chat_photo", None)
        self.deleteChatPhoto = kwargs.get("delete_chat_photo", None)
        self.groupChatCreated = kwargs.get("group_chat_created", None)
        self.supergroupChatCreated = kwargs.get("supergroup_chat_created", None)
        self.channelChatCreated = kwargs.get("channel_chat_created", None)
        self.messageAutoDeleteTimerChanged = kwargs.get(
            "message_auto_delete_timer_changed", None
        )
        self.migrateToChatId = kwargs.get("migrate_to_chat_id", None)
        self.migrateFromChatId = kwargs.get("migrate_from_chat_id", None)
        self.pinnedMessage = kwargs.get("pinned_message", None)
        self.invoice = kwargs.get("invoice", None)
        self.successfulPayment = kwargs.get("successful_payment", None)
        self.usersShared = kwargs.get("users_shared", None)
        self.chatShared = kwargs.get("chat_shared", None)
        self.connectedWebsite = kwargs.get("connected_website", None)
        self.writeAccessAllowed = kwargs.get("write_access_allowed", None)
        self.passportData = kwargs.get("passport_data", None)
        self.proximityAlertTriggered = kwargs.get("proximity_alert_triggered", None)
        self.boostAdded = kwargs.get("boost_added", None)
        self.chatBackgroundSet = kwargs.get("chat_background_set", None)
        self.forumTopicCreated = kwargs.get("forum_topic_created", None)
        self.forumTopicEdited = kwargs.get("forum_topic_edited", None)
        self.forumTopicClosed = kwargs.get("forum_topic_closed", None)
        self.forumTopicReopened = kwargs.get("forum_topic_reopened", None)
        self.generalForumTopicHidden = kwargs.get("general_forum_topic_hidden", None)
        self.generalForumTopicUnhidden = kwargs.get(
            "general_forum_topic_unhidden", None
        )
        self.giveawayCreated = kwargs.get("giveaway_created", None)
        self.giveaway = kwargs.get("giveaway", None)
        self.giveawayWinners = kwargs.get("giveaway_winners", None)
        self.giveawayCompleted = kwargs.get("giveaway_completed", None)
        self.videoChatScheduled = kwargs.get("video_chat_scheduled", None)
        self.videoChatStarted = kwargs.get("video_chat_started", None)
        self.videoChatEnded = kwargs.get("video_chat_ended", None)
        self.videoChatParticipantsInvited = kwargs.get(
            "video_chat_participants_invited", None
        )
        self.webAppData = kwargs.get("web_app_data", None)
        self.replyMarkup = kwargs.get("reply_markup", None)

    def parseMessage(self, message: object):
        self.message = message
        try:
            return self.message.__dict__
        except AttributeError:
            return self.message
