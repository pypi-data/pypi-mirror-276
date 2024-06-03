import os
import json
import grambot

from .exception import GrambotError


class Session:
    def __init__(self, client: "grambot.GramClient", name: str):
        self.name = name
        self.client = client

    def create_instance(self):
        self.client.sessionName = self.name + ".session"
        if os.path.exists(self.client.sessionName):
            os.remove(self.client.sessionName)

        instance = open(self.client.sessionName, mode='w')
        data = json.dumps({
            'name': self.client.name,
            'token': self.client.token,
            'parse_mode': self.client.parse_mode,
        })
        instance.write(data)


    def delete_instance(self):
        if os.path.exists(self.client.sessionName):
            os.remove(self.client.sessionName)


    def get_current_instance(self) -> "grambot.GramClient":
        try:
            with open(self.client.sessionName, mode='r') as f:
                data = json.loads(f.read())
                bot = grambot.GramClient(
                    name=data.get('name'),
                    token=data.get('token'),
                    parse_mode=data.get('parse_mode'),
                )
                return bot
        except FileNotFoundError:
            raise GrambotError("Session not found, Please run 'await grambot.start()' first")
