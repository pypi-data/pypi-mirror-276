from .onCallbackQuery import OnCallbackQuery
from .onInlineQuery import OnInlineQuery
from .onMessage import OnMessage


class Decorators(
    OnCallbackQuery,
    OnInlineQuery,
    OnMessage
):
    pass
