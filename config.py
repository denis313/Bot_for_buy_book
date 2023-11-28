from environs import Env
from aiogram import Bot, Dispatcher

env = Env()
env.read_env()

bot_token = '6929515792:AAF78OQy867ZgnX_cj_ihILEX_91hbYNzZ8'
# ykassa = env('YKASSA')
admins_ids = [1087502760]

bot: Bot = Bot(token=bot_token)
dp: Dispatcher = Dispatcher()
