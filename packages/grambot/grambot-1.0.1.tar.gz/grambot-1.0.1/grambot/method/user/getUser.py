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

from typing import Union

import grambot
from grambot.types import User


class GetUser:
    async def getUser(self: "grambot.GramClient", userId: Union[int, str]) -> "User":
        self.userId = userId
        if isinstance(self.userId, int):
            if userId == -100:
                return ValueError("Invalid user id")
        params = {"user_id": userId}
        user = self.api._method("getChat", params=params)
        return User(**user)
