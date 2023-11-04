from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


'''   
        Создание обьект основной клавиатуры Админа и кнопок для основной клавиатуры Admin
'''
btn_1 = KeyboardButton(text='Список книг в базе 📚')
btn_2 = KeyboardButton(text='Добавить книгу ✅')
btn_3 = KeyboardButton(text='Удалить книгу ❌')


keyboard_for_admin = ReplyKeyboardMarkup(keyboard=[[btn_1, btn_2], [btn_3]],
                                         resize_keyboard=True)
