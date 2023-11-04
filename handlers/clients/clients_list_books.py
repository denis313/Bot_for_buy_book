from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import bot
from data_base.buy_books_bd_for_books import get_all_books, get_book, search_for_book_in_bd
from data_base.buy_books_bd_users import update_basket, getting_information_from_the_cart
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice, SuccessfulPayment
from keyboards.buy_books_keyboard import keyboard_for_book, main_keyboard, stop_fsm, keyboard_book
from filters_for_handler.Admin_filter import BuyNow, InBasket

router = Router()


@router.message(F.text == 'Список книг')
async def list_books(message: Message):
    all_books = get_all_books()
    # print(all_books)
    for book in all_books:
        id_book, name, author, description, price, photo = book
        await message.answer_photo(photo=photo, caption=f'<b>Название:</b> {name.capitalize()}\n'
                                                        f'<b>Автор:</b> {author.title()}\n'
                                                        f'<b>Описание:</b> {description.capitalize()}\n'
                                                        f'<b>Цена:</b> {price}',
                                                        reply_markup=keyboard_for_book(id_book=id_book),
                                                        parse_mode='HTML')


@router.callback_query(BuyNow())
async def buy_now(callback: CallbackQuery):
    id_book = int(callback.data.replace('buy', ''))
    user_id = callback.from_user.id
    book = get_book(id_book=id_book)
    name, author, price, photo = book
    await bot.send_invoice(chat_id=user_id,
                           need_name=True,
                           need_email=True,
                           need_phone_number=True,
                           title=f'Покупка "{name.capitalize()}"',
                           description=f'Вы покупаете книгу: {name.capitalize()}',
                           provider_token="381764678:TEST:67414",
                           currency='RUB',
                           payload=f'buy_book{id_book}',
                           start_parameter='text',
                           prices=[
                               LabeledPrice(label="rub",
                                            amount=int(price) * 100)])


@router.callback_query(InBasket())
async def buy_now(callback: CallbackQuery):
    id_book = int(callback.data.replace('in', ''))
    user_id = callback.from_user.id
    name, author, price, photo = get_book(id_book=id_book)
    if f' {name} {author} {price};' in getting_information_from_the_cart(user_id=callback.from_user.id)[0]:
        await callback.answer('Книга уже есть в корзине)')
    else:
        update_basket(user_id, name.capitalize(), author.title(), price)
        await callback.answer('Книга добавлена в корзину)')


class Search(StatesGroup):
    name = State()
    author = State()


@router.message(F.text == 'Stop')
async def process_gender_press(message: Message, state: FSMContext):
    await message.answer('Заполние прекращено', reply_markup=main_keyboard)
    await state.clear()


@router.message(F.text == 'Поиск')
async def search_book(message: Message, state: FSMContext):
    await state.set_state(Search.name)
    await message.answer(text="Отправьте название книги:", reply_markup=stop_fsm())


@router.message(Search.name)
async def search_name_book(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Search.author)
    await message.answer('Введите автора книги:')


@router.message(Search.author)
async def search_author_book(message: Message, state: FSMContext):
    await state.update_data(author=message.text)
    data = await state.get_data()
    await state.clear()
    search_results = search_for_book_in_bd(data['name'], data['author'])
    if search_results:
        name, author, description, price, photo = search_results
        await message.answer_photo(photo=photo, caption=f'<b>Название:</b> {name.capitalize()}\n'
                                                        f'<b>Автор:</b> {author.title()}\n'
                                                        f'<b>Описание:</b> {description.capitalize()}\n'
                                                        f'<b>Цена:</b> {price}',
                                   parse_mode='html',
                                   reply_markup=main_keyboard)
    else:
        await message.answer("Такой книги нет😭", reply_markup=main_keyboard)


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
    books_basket, total_amount = getting_information_from_the_cart(user_id=user_id)
    await bot.send_invoice(chat_id=user_id,
                           need_name=True,
                           need_email=True,
                           need_phone_number=True,
                           title=f'Покупка "Все книги"',
                           description=f'Вы покупаете книгу все книги из корзины',
                           provider_token="381764678:TEST:67414",
                           currency='RUB',
                           payload='buy_book',
                           start_parameter='text',
                           prices=[
                               LabeledPrice(label="rub",
                                            amount=int(total_amount) * 100)])


@router.pre_checkout_query(lambda query: True)
async def process_pre_check(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# @router.message(SuccessfulPayment)
# async def process_puy(message: Message):
#     print(message.successful_payment)
#     if message.successfulpayment.invoice_payload == 'buy_book':
#         await bot.send_message(message.chat.id, 'Successful!')
#         books = getting_information_from_the_cart(user_id=message.from_user.id)
#         books_for_buy = books[0].split(';')[0:-1]
#         await bot.send_message(-1001790065720,
#                                f'{message.first_name, message.last_name, message.username} {books_for_buy}')
#     else:
#         name, author, price, photo = get_book(id_book=int(message.successful_payment.invoice_payload.replace("payload", "")))
#         await bot.send_message(-1001790065720,
#                                f'{message.first_name, message.last_name, message.username} '
#                                f'{name, author, price}')
