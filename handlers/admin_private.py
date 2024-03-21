from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import orm_add_product, orm_get_products

from filters.chat_types import ChatTypeFilter, IsAdmin
from keyboards.inline import get_callback_btns
from keyboards.reply import get_keyboard


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(['private']), IsAdmin()) # Встановлюємо фільтр до роутера, який буде автоматично викликати функцію ChatTypeFilter() для кожного повідомлення в приватному чаті   

ADMIN_KB = get_keyboard(
    'Додати товар',
    'Список товарів',
    placeholder='Оберіть дію',
    sizes=(2,),
)

@admin_router.message(Command('admin'))
async def add_product(message: types.Message):
    await message.answer('Виберіть наступну дію:', reply_markup=ADMIN_KB)



@admin_router.message(F.text == 'Список товарів')
async def show_products(message: types.Message, session: AsyncSession):
    for product in await orm_get_products(session):
        await message.answer_photo(
            product.image,
            caption=f"<strong>{product.name}\
                </strong>\n{product.description}\nЦіна: {product.price}",
            reply_markup=get_callback_btns(btns={
                'Видалити': f'delete_{product.id}',
                'Змінити': f'change_{product.id}'
            })
        )
    await message.answer('Ось список товарів:')




#Код для машини стану (FSM)
    
class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    text = {
        'AddProduct:name': 'Введіть назву товару повторно:',
        'AddProduct:description': 'Введіть опис товару повторно:',
        'AddProduct:price': 'Введіть ціну товару повторно:',
        'AddProduct:image': 'Це останній крок. Завантажте фото товару:'
    }


@admin_router.message(StateFilter(None), F.text == 'Додати товар')
async def add_prosduct(message: types.Message, state: FSMContext):
    await message.answer('Введіть назву товару:', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.name)

@admin_router.message(StateFilter('*'), Command('відмінити'))
@admin_router.message(StateFilter('*'), F.text.casefold() == 'відмінити')
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer('Ви відмінили дію', reply_markup=ADMIN_KB)

@admin_router.message(StateFilter('*'), Command('назад'))
@admin_router.message(StateFilter('*'), F.text.casefold() == 'назад')
async def step_back_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await message.answer('Кроків назад вже немає. Додайте назву товару або натисність "Відмінити"')
        return
    
    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f'Ви повернулись на крок назад \n {AddProduct.text[previous]}')
            return
        previous = step

@admin_router.message(AddProduct.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введіть опис товару')
    await state.set_state(AddProduct.description) 

@admin_router.message(AddProduct.name)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer('Ви вказали некоректну назву товару. Введіть назву товару повторно:') 

@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Введіть ціну товару')
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.description)
async def add_description(message: types.Message, state: FSMContext):
    await message.answer('Ви вказали некоректні дані. Введіть опис товару повторно:')

@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=f'{message.text} грн')
    await message.answer('Завантажте фото товару')
    await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.price)
async def add_price(message: types.Message, state: FSMContext):
    await message.answer('Ви вказали некоректну ціну товару. Введіть ціну товару повторно:')

@admin_router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        await orm_add_product(session, data)
        await message.answer('Товар додано', reply_markup=ADMIN_KB)
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Помилка: \n{str(e)}\nСпробуйте ще раз.", reply_markup=ADMIN_KB)
        await state.clear()
        

@admin_router.message(AddProduct.image)
async def add_image2(message: types.Message, state: FSMContext):
    await message.answer("Отправьте фото пищи")


