from aiogram.filters.callback_data import CallbackData


# Класс для создания callback_data для покупки книги сразу
class BuyCallbackFactory(CallbackData, prefix='buy'):
    id_book: int


# Класс для создания callback_data для добавления книги в коризну
class InBasketCallbackFactory(CallbackData, prefix='in_basket'):
    id_book: int
