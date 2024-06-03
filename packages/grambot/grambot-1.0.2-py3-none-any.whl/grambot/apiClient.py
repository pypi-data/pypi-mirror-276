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

from requests import post


class ApiClient:
    def __init__(self, token: str):
        self.token = token
        self._base_url = f"https://api.telegram.org/bot{self.token}/"
        self._base_url_file = f"https://api.telegram.org/file/bot{self.token}/"

    def _method(self, method: str, params: dict = None, file: bool = False):
        if file:
            baseUrl = self._base_url_file
        else:
            baseUrl = self._base_url
        if params is None:
            params = ""
        else:
            params = f"?{('&'.join([f'{k}={v}' for k, v in params.items()]))}"
        response = post(
            url=f"{baseUrl}{method}{params}",
            headers={"Content-Type": "application/json"},
        )
        res = response.json()
        if res.get("ok"):
            return res.get("result")
        else:
            error = res.get("description")
            raise Exception(error)
