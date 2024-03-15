from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command

user_private_router = Router()


@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Привіт, я твій віртуальний помічний')

@user_private_router.message(Command('menu'))
async def menu_cmd(message: types.Message):
    await message.answer('Ось меню: \n')

@user_private_router.message(Command('about'))
async def about_cmd(message: types.Message):
    await message.answer('Про бота: \n')
    await message.answer('Цей бот створений для того, щоб допомогти вам створити список страв для приготування протягом тижня. \n')

@user_private_router.message(Command('payment'))
async def payment_cmd(message: types.Message):
    await message.answer('Варіанти оплати: \n')

@user_private_router.message(Command('shipping'))
async def shipping_cmb(message: types.Message):
    await message.answer('Способи доставки: \n')

@user_private_router.message(F.text.lower() == 'варіанти доставки') # Магічний фільтр для текстових повідомлень
async def shipping_cmb(message: types.Message):
    await message.answer('Магічний фільтр для текстових повідомлень')