from environs import Env
from aiogram import Bot, Dispatcher

env = Env()
env.read_env()

bot_token = '5196838263:AAGqNO2Q-BpsQHgKhTf4DZDQt-e4TLQRKkU'
# ykassa = env('YKASSA')
admins_ids = [1087502760]

bot: Bot = Bot(token=bot_token)
dp: Dispatcher = Dispatcher()
