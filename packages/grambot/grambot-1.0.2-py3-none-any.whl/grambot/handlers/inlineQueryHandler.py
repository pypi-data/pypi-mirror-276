import asyncio
import re

from typing import Callable

import grambot

from .handler import Handler
from ..types import InlineQuery


class InlineQueryHandler(Handler):
    def __init__(self, callback: Callable, filters=None):
        super(InlineQueryHandler, self).__init__(callback, filters)
        self.required_filters = ['regex']
    
    async def check(self, bot: 'grambot.GramClient', update):
        if isinstance(update, InlineQuery):
            if self.filters:
                filter_type = self.filters.get('type')
                if filter_type and filter_type in self.required_filters:
                    if update.query:
                        regex = self.filters.get('regex')
                        m = re.search(regex, update.query, re.I)
                        if m:
                            return True
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