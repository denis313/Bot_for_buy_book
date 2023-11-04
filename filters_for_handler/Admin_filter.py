from aiogram.filters import Filter, BaseFilter
from aiogram.types import Message, CallbackQuery

# admin_ids: list[int] = [1087502760]


class IsAdmin(Filter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, message: Message) -> bool:
        print(message.from_user.id in self.admin_ids)
        return message.from_user.id in self.admin_ids


class BuyNow(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('buy')


class InBasket(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data.endswith('in')
