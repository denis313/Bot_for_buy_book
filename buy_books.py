import asyncio
from config import bot, dp
from handlers.admin import admin_list_books, admin_add_book, admin_del_book
from handlers.clients import clients_list_books
from handlers import start_bot_command


# Основная функция
async def main():
    dp.include_router(start_bot_command.router)
    dp.include_routers(admin_list_books.router,
                       admin_add_book.router,
                       admin_del_book.router)
    dp.include_router(clients_list_books.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    print('work')
    asyncio.run(main())
