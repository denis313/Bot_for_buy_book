from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from data_base.buy_books_bd_for_books import add_new_book
from keyboards.keyboard_for_admin import keyboard_for_admin
from keyboards.buy_books_keyboard import stop_fsm
from config import admins_ids


router = Router()
# admin_ids = [1087502760]
# router.message.filter(IsAdmin(admin_ids))

'''                                         Добавление новой книги                                '''


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    author = State()
    description = State()
    price = State()


@router.message(F.text == 'Stop 🛑')
async def process_gender_press(message: Message, state: FSMContext):
    await message.answer('Заполние прекращено', reply_markup=keyboard_for_admin)
    await state.clear()


@router.message(F.text == 'Добавить книгу ✅')
async def add_book(message: Message, state: FSMContext):
    if message.from_user.id in admins_ids:
        await state.set_state(FSMAdmin.name)
        await message.answer(text="Загрузите название:", reply_markup=stop_fsm())


@router.message(FSMAdmin.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FSMAdmin.author)
    await message.answer('Введите автора книги:')


@router.message(FSMAdmin.author)
async def add_author(message: Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(FSMAdmin.description)
    await message.answer('Введите описание книги:')


@router.message(FSMAdmin.description)
async def add_description(message: Message, state: FSMContext):
    if len(message.text) < 15:
        await message.answer('Описание книги должно быть информативным')
    else:
        await state.update_data(description=message.text)
        await state.set_state(FSMAdmin.price)
        await message.answer('Введите цену книги:')


@router.message(FSMAdmin.price)
async def add_description(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(price=message.text)
        await state.set_state(FSMAdmin.photo)
        await message.answer('Загрузите фото:')
    else:
        await message.answer('Введите цену книги:')


@router.message(FSMAdmin.photo, F.photo)
async def add_photo(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    await state.clear()
    book = {}

    for key, value in data.items():
        book[key] = value
    # print(book)
    await message.answer_photo(photo=photo, caption=f'<b>Название:</b> {book["name"].capitalize()}\n'
                                                    f'<b>Автор:</b> {book["author"].title()}\n'
                                                    f'<b>Описание:</b> {book["description"].capitalize()}\n'
                                                    f'<b>Цена:</b> {book["price"]}', reply_markup=keyboard_for_admin,
                               parse_mode='html')
    add_new_book(name=book['name'],
                 author=book['author'],
                 description=book['description'],
                 price=book['price'],
                 photo=photo)


@router.message(FSMAdmin.photo, ~F.photo)
async def add_photo(message: Message, state: FSMContext):
    await message.answer('Загрузите фото:')
