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


class UserProfilePhotos:
    def __init__(self, **kwargs) -> None:
        self.photos = kwargs.get("photos", None)
        self.totalCount = kwargs.get("total_count", None)

    def parseUserProfilePhotos(self, userProfilePhotos: object):
        self.userProfilePhotos = userProfilePhotos
        try:
            self.userProfilePhotos.__dict__
        except AttributeError:
            return self.userProfilePhotos
