import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart


bot = Bot(token='6962523796:AAH2A3gODWvm9s0c-DqKAraAKQ534Obwj8g')

dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Hello')

@dp.message()
async def echo(message):
    await message.answer(message.text)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())