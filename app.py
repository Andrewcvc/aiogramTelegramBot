import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import BotCommandScopeAllPrivateChats

from dotenv import find_dotenv, load_dotenv

from middlewares.db import DataBaseSession # Для зчитування змінних середовища з .env файлу

load_dotenv(find_dotenv()) # Завантажуємо змінні середовища з .env файлу


from database.engine import create_db, drop_db, session_maker # Імпортуємо функції create_db, drop_db, session_maker з файлу database/engine.py


from handlers.user_private import user_private_router # Імпортуємо роутер user_private_router з файлу handlers/user_private.py  
from handlers.user_group import user_group_router
from handlers.admin_private import admin_router
from common.bot_cmds_list import private_commands # Імпортуємо список команд бота для приватних чатів з файлу common/bot_cmds_list.py
from aiogram.enums import ParseMode


ALLOWED_UPDATES = ['message', 'edited_message'] # Список типів оновлень які бот буде обробляти. Це може бути список з такими типами: ['message', 'edited_message', 'channel_post', 'edited_channel_post', 'inline_query', 'chosen_inline_result', 'callback_query', 'shipping_query', 'pre_checkout_query', 'poll', 'poll_answer', 'my_chat_member', 'chat_member'
bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML) # Створюємо об'єкт бота з токеном який зчитуємо з змінних середовища
bot.my_admin_list = []

dp = Dispatcher()

dp.include_router(user_private_router) # Підключаємо роутер user_private_router до диспетчера dp     
dp.include_router(user_group_router)
dp.include_router(admin_router)

async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()
    
    await create_db()

async def on_shutdown(bot):
    print('Shutting down..')


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True) # Скидує всі оновлення(повідомлення від користувачів в боті) які були в черзі поки бот був виключений. І дає можливість боту відповісти на останні оновлення
    await bot.set_my_commands(commands=private_commands, scope=types.BotCommandScopeAllPrivateChats()) # Встановлюємо команди бота для приватних чатів. Параметр commands - це список команд які буде виконувати бот. Параметр scope - це область видимості команд. В даному випадку команди будуть видимі тільки в приватних чатах
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES) #allowed_updates - це список типів оновлень які бот буде обробляти. Якщо не вказати цей параметр, то бот буде обробляти всі типи оновлень

asyncio.run(main())