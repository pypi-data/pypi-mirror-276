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

class Webhook:
    async def setWebhook(
        self: "grambot.GramClient",
        url: str,
        certificate: str = None,
        maxConnections: int = None,
        allowedUpdates: list = None,
        ipAddress: str = None,
        dropPendingUpdates: bool = None,
        secretToken: str = None,
    ):
        self.ceritificate = certificate
        self.maxConnections = maxConnections
        self.allowedUpdates = allowedUpdates
        self.ipAddress = ipAddress
        self.dropPendingUpdates = dropPendingUpdates
        self.secretToken = secretToken
        self.url = url
        self.params: dict = {}
        if self.ceritificate:
            self.params["certificate"] = self.ceritificate
        if self.maxConnections:
            self.params["max_connections"] = self.maxConnections
        if self.allowedUpdates:
            self.params["allowed_updates"] = self.allowedUpdates
        if self.ipAddress:
            self.params["ip_address"] = self.ipAddress
        if self.dropPendingUpdates:
            self.params["drop_pending_updates"] = self.dropPendingUpdates
        if self.secretToken:
            self.params["secret_token"] = self.secretToken
        await self.start()
        response = self.api._method("setWebhook", self.params)
        return response

    async def deleteWebhook(self: "grambot.GramClient"):
        return self.api._method("deleteWebhook")

    async def getWebhookInfo(self: "grambot.GramClient"):
        return self.api._method("getWebhookInfo")