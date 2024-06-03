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


import grambot
from grambot.types.users import UserProfilePhotos


class GetUserProfilePhotos:
    async def getUserProfilePhotos(self, user_id: int, offset: int = None, limit: int = None) -> "UserProfilePhotos":
        self.userId = user_id
        self.offset = offset
        self.limit = limit
        self.params = {}
        self.params["user_id"] = self.userId
        if self.offset:
            self.params["offset"] = self.offset
        if self.limit:
            self.params["limit"] = self.limit
        data = await self.api._method("getUserProfilePhotos", self.params)
        return UserProfilePhotos(**data)
