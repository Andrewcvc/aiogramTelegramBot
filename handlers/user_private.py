from aiogram import F, types, Router
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.formatting import as_list, as_marked_section, Bold, Italic
from sqlalchemy.ext.asyncio import AsyncSession


from database.orm_query import orm_get_products
from filters.chat_types import ChatTypeFilter
from keyboards.reply import get_keyboard


user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private'])) # Встановлюємо фільтр до роутера, який буде автоматично викликати функцію ChatTypeFilter() для кожного повідомлення в приватному чаті

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        'Привіт, я твій віртуальний помічний',
        reply_markup=get_keyboard(
            'Меню',
            'Про бота',
            'Варіанти оплати',
            'Варіанти доставки',
            "Відправити номер телефону ☎️",
            "Відправити місцезнаходження 🗺️",
            request_contact=4,
            request_location=5,
            placeholder='Що вас цікавить?',
            sizes=(2, 2, 1, 1)
        ),
    )


@user_private_router.message(or_f(Command('menu'), (F.text.lower() == 'меню'))) # or_f - це логічний оператор "або" для фільтрів
async def menu_cmd(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                </strong>\n{product.description}\nЦіна: {product.price}",
        )
    await message.answer('Ось меню: \n')

@user_private_router.message(or_f(Command('about'), (F.text.lower() == 'про бота')))
async def about_cmd(message: types.Message):
    await message.answer('Про бота: \n \nЦей бот створений для того, щоб допомогти вам створити список страв для приготування протягом тижня.')
    # await message.answer('Цей бот створений для того, щоб допомогти вам створити список страв для приготування протягом тижня. \n')

@user_private_router.message(or_f(Command('payment'), (F.text.lower().contains('оплат')), (F.text.lower() == 'варіанти оплати')))
async def payment_cmd(message: types.Message):
    text = as_marked_section(
        Bold('Варіанти оплати:'),
        'Готівкою при отриманні',
        'Карткою Visa/MasterCard',
        'Онлайн-оплата',
        marker='✅ '
    )
    await message.answer(text.as_html())

@user_private_router.message(or_f(Command('shipping'), (F.text.lower().contains('доставк')), (F.text.lower() == 'варіанти доставки')))
async def shipping_cmb(message: types.Message):
    text = as_list(
        as_marked_section(
            Bold('Способи доставки:'),
            'Кур\'єром',
            'Самовивіз',
            'Нова Пошта',
            marker='✉️ '
        ),
        as_marked_section(
            Bold('Терміни доставки:'),
            '1-2 дні',
            '2-3 дні',
            '3-5 днів',
            marker='📆 '
        ),
        sep='\n--------------------------------\n'
    )
    await message.answer(text.as_html())

@user_private_router.message(F.contact)
async def get_contact(message: types.Message):
    await message.answer(f"Ваш номер отриманий")
    await message.answer(str(message.contact.phone_number), protect_content=True)

@user_private_router.message(F.location)
async def get_location(message: types.Message):
    await message.answer(f"Ваше місцезнаходження отримано")

