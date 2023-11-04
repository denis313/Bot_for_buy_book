from aiogram import Router
from aiogram.filters import Command, CommandStart
from data_base.buy_books_bd_users import new_user
from aiogram.types import Message
from keyboards.buy_books_keyboard import main_keyboard
from keyboards.keyboard_for_admin import keyboard_for_admin
from config import admins_ids


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    if message.from_user.id in admins_ids:
        await message.answer('Вы администратор\n'
                             'Можно добавлять и удалять книги', reply_markup=keyboard_for_admin)
    else:
        await message.answer('Бот позволяет покупать христианскую литературу прямо в телеграме\n\n'
                             'Используйте клавиатуру для взаимодействия с Ботом\n\n'
                             'Если что-то не понятно отправь команду /help', reply_markup=main_keyboard)
        user_id: int = message.from_user.id
        ''' Добавление пользователя в Базу Данных'''
        new_user(user_id=user_id)


@router.message(Command('help'))
async def process_help_command(message: Message):
    await message.answer('<b>Список книг</b> - возможность посмотреть существующие книги\n'
                         '<b>Поиск</b> - возможность найти книгу по ее названию и автору\n'
                         '<b>Корзина</b> - возможность посмотреть книги которые вы выбрали для покупки', parse_mode='HTML')
