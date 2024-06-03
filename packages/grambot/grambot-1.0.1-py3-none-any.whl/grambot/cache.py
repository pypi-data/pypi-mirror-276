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

class Cache:
    _storage = {}
    def __init__(self, name: str):
        self.name = name
        self.db: dict = self._storage.get(self.name, {})

    def __getitem__(self, key):
        return self.db.get(key, None)

    def __setitem__(self, key, value):
        if key in self.db:
            del self.db[key]

        self.db[key] = value

    def __delitem__(self, key):
        del self.db[key]