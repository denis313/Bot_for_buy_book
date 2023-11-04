from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from data_base.buy_books_bd_for_books import get_all_books, delete_book
from keyboards.keyboard_for_admin import keyboard_for_admin
from keyboards.buy_books_keyboard import stop_fsm
from config import admins_ids


router = Router()

'''                                         Удаление книги                                '''


class BookForDel(StatesGroup):
    id_book = State()


@router.message(F.text == 'Stop 🛑')
async def process_gender_press(message: Message, state: FSMContext):
    await message.answer('Заполние прекращено', reply_markup=keyboard_for_admin)
    await state.clear()


@router.message(F.text == 'Удалить книгу ❌')
async def del_book(message: Message, state: FSMContext):
    if message.from_user.id in admins_ids:
        await state.set_state(BookForDel.id_book)
        await message.answer('Отправь id_book', reply_markup=stop_fsm())


@router.message(BookForDel.id_book)
async def id_book(message: Message, state: FSMContext):
    if int(message.text) <= len(get_all_books()):
        await state.update_data(id_book=message.text)
        data = await state.get_data()
        await state.clear()
        delete_book(data['id_book'])
        await message.answer(f'Книга с {data["id_book"]} успешна удалена', reply_markup=keyboard_for_admin)
    else:
        await message.answer('Вашего id_book не существует\n'
                             'Отправьте корректный id_book', reply_markup=keyboard_for_admin)