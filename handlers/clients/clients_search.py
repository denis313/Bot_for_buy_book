from aiogram import F, Router
from data_base.buy_books_bd_for_books import search_for_book_in_bd
from aiogram.types import Message
from keyboards.buy_books_keyboard import main_keyboard, stop_fsm
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()


class Search(StatesGroup):
    name = State()
    author = State()


@router.message(F.text == 'Stop 🛑')
async def process_gender_press(message: Message, state: FSMContext):
    await message.answer('Заполние прекращено', reply_markup=main_keyboard)
    await state.clear()


@router.message(F.text == 'Поиск 🔎')
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
