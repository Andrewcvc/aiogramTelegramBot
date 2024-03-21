from string import punctuation
from aiogram import F, types, Router, Bot
from filters.chat_types import ChatTypeFilter
from aiogram.filters import Command

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup'])) # Встановлюємо фільтр для групових чатів

restricted_words = {'блять', 'сука', 'хуй', 'підр'}

@user_group_router.message(Command('admin'))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()



def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation)) # Видаляємо всі знаки пунктуації з тексту щоб люди які хочуть зашифрувати заборонені слова символами, не могли це зробити

@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(clean_text(message.text.lower()).split()): # split() - розбиває текст на слова і повертає список цих слів
        await message.answer(f"{message.from_user.first_name}, ви використали недопустимі слова! Ваше повідомлення видалено.")
        await message.delete()
        # await message.chat.ban(message.from_user.id) 