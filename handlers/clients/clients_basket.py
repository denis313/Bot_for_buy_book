from aiogram import F, Router
from config import bot
from data_base.buy_books_bd_for_books import get_book
from data_base.buy_books_bd_users import getting_information_from_the_cart
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice, SuccessfulPayment
from keyboards.buy_books_keyboard import keyboard_book

router = Router()


@router.message(F.text == 'Корзина')
async def basket_of_cart(message: Message):
    user_id = message.from_user.id
    books = getting_information_from_the_cart(user_id=user_id)
    books_for_buy = books[0].split(';')[0:-1]
    await message.answer(f'Общая стоимость книг в корзине - {books[1]}', reply_markup=keyboard_book)
    for book in books_for_buy:
        await message.answer(book)


# async def add_basket(callback: CallbackQuery):
#     user_id = callback.from_user.id
#     update_basket(user_id=user_id, name=, author=, price=)


@router.callback_query(F.data == 'buy_all_books')
async def process_buy_books(callback: CallbackQuery):
    user_id = callback.from_user.id
    total = getting_information_from_the_cart(user_id=user_id)
    await bot.send_invoice(chat_id=callback.from_user.id,
                           title='Покупка всех книг',
                           description='Вы покупаете все книги из карзины',
                           payload='buy_book',
                           provider_token="381764678:TEST:67414",
                           currency='RUB',
                           start_parameter='text',
                           prices=[
                               LabeledPrice(label="rub",
                                            amount=total[1]*100)]
                           )


@router.pre_checkout_query(lambda query: True)
async def process_pre_check(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@router.message(SuccessfulPayment)
async def process_puy(message: Message):
    print('SP')
    if message.successful_payment.invoice_payload == 'buy_book':
        await bot.send_message(message.chat.id, 'Successful!')
        books = getting_information_from_the_cart(user_id=message.from_user.id)
        books_for_buy = books[0].split(';')[0:-1]
        await bot.send_message(-1001790065720,
                               f'{message.first_name, message.last_name, message.username} {books_for_buy}')
    else:
        name, author, price, photo = get_book(id_book=int(message.successful_payment.invoice_payload.replace("payload", "")))
        await bot.send_message(-1001790065720,
                               f'{message.first_name, message.last_name, message.username} '
                               f'{name, author, price}')
