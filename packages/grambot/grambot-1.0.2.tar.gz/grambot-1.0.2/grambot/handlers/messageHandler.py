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

import re
import json

from typing import Callable

import grambot

from .handler import Handler
from ..types import Message


class MessageHandler(Handler):
    def __init__(self, callback: Callable, filters=None):
        super(MessageHandler, self).__init__(callback, filters)
        self.exclude = ['callback_data']
        self.special_types = ['command', 'all', 'regex', 'text', 'chat']

    async def check(self, bot: 'grambot.GramClient', update):
        if isinstance(update, Message):
            if self.filters:
                filter_type = self.filters.get('type')
                update_json = json.loads(update.json())
                if filter_type:
                    if filter_type not in self.special_types and filter_type not in self.exclude:
                        if update_json.get(filter_type):
                            return True
                        else:
                            return False
                    elif filter_type in self.special_types:
                        if filter_type == "command":
                            prefixes = self.filters.get('prefix')
                            commands = self.filters.get('command')
                            if update.text:
                                if type(prefixes) is str:
                                    if update.text.startswith(prefixes):
                                        pass
                                    else:
                                        return False
                                else:
                                    for pre in prefixes:
                                        if update.text.startswith(pre):
                                            pass
                                        else:
                                            return False

                                if type(commands) is str:
                                    m = re.search(commands, update.text, re.I)
                                    if m:
                                        return True
                                    else:
                                        return False
                                else:
                                    for command in commands:
                                        m = re.search(command, update.text, re.I)
                                        if m:
                                            return True
                                        else:
                                            return False
                        elif filter_type == 'regex':
                            regex = self.filters.get('regex')
                            if update.text:
                                m = re.search(regex, update.text, re.I)
                                if m:
                                    return True
                                else:
                                    return False
                        elif filter_type == 'text':
                            text = self.filters.get('text')
                            if update.text:
                                if text:
                                    m = re.search(text, update.text, re.I)
                                    if m:
                                        return True
                                    else:
                                        return False
                                else:
                                    return True
                        elif filter_type == 'chat':
                            chat_type = self.filters.get('chat_type')
                            if update.chat.type == chat_type:
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return True
        else:
            return False
