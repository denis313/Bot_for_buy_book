from aiogram import F, Router
from aiogram.types import Message
from data_base.buy_books_bd_for_books import get_all_books
from config import admins_ids


router = Router()

'''                                         Список книг в базе                                '''


@router.message(F.text == 'Список книг в базе')
async def all_book_for_admin(message: Message):
    if message.from_user.id in admins_ids:
        all_books = get_all_books()
        for book in all_books:
            id_book, name, author, description, price, photo = book
            await message.answer_photo(photo=photo, caption=f'id_book книги: <b>{id_book}</b>\n'
                                                            f'Название: {name.capitalize()}\n'
                                                            f'Автор: {author.title()}',
                                       parse_mode='HTML')





# @router.message(BookForDel.id_book, F)
# async def add_photo(message: Message, state: FSMContext):
#     await message.answer('Отправьте id_book:')
