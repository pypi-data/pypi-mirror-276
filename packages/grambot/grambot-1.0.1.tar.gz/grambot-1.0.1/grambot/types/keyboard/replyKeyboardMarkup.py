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


class ReplyKeyboardMarkup:
    def __init__(self, **kwargs):
        self.keyboard = kwargs.get("keyboard", None)
        self.isPersistent = kwargs.get("is_persistent", None)
        self.resizeKeyboard = kwargs.get("resize_keyboard", None)
        self.oneTimeKeyboard = kwargs.get("one_time_keyboard", None)
        self.inputFieldPlaceholder = kwargs.get("input_field_placeholder", None)
        self.selective = kwargs.get("selective", None)

    @classmethod
    def parseReplyMarkup(cls, reply_markup: object):
        if reply_markup is None:
            return None
        else:
            return cls(**reply_markup)