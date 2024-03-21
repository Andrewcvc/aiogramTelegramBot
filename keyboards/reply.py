from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_keyboard(
        *btns: str,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,),
):
    # Ця функція повертає клавіатуру з кнопками
    #request_contact, request_location треба вказувати як індекс кнопок записаних у функції
    # напкриклад:
    # get_keyboard(
    #     'Меню',              [0]
    #     'Про бота',          [1]
    #     'Варіанти оплати',   [2]
    #     'Варіанти доставки', [3]
    #     "Відправити номер телефону ☎️",   [4]
    #     "Відправити місцезнаходження 🗺️"   [5]
    #     sizes=(2, 2, 1, 1)   
    # )
    keyboard = ReplyKeyboardBuilder()

    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index: 
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        
        elif request_location and request_location == index: # Якщо request_location індекс кнопки
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text)) # Додаємо кнопку в клавіатуру

    return keyboard.adjust(*sizes).as_markup(resize_keyboard=True, input_field_placeholder=placeholder) # Повертаємо клавіатуру з кнопками



# start_kb = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="Меню"),
#             KeyboardButton(text="Про бота"),
#         ],
#         [
#             KeyboardButton(text="Варіанти оплати"),
#             KeyboardButton(text="Варіанти доставки")
#         ]
#     ],
#     resize_keyboard=True,
#     input_field_placeholder='Що вас цікавить?'
# )

# del_kbd = ReplyKeyboardRemove()

# start_kb2 = ReplyKeyboardBuilder()
# start_kb2.add(
#     KeyboardButton(text="Меню"),
#     KeyboardButton(text="Про бота"),
#     KeyboardButton(text="Варіанти оплати"),
#     KeyboardButton(text="Варіанти доставки"),
#     KeyboardButton(text="Відправити номер телефону ☎️", request_contact=True),
#     KeyboardButton(text="Відправити місцезнаходження 🗺️", request_location=True)
# )

# start_kb2.adjust(2, 2, 1, 1) # Змінюємо розмір клавіатури на 3 рядки і 3 стовпці


# start_kb3 = ReplyKeyboardBuilder()
# start_kb3.attach(start_kb2)  # Додаємо клавіатуру start_kb2 до клавіатури start_kb3
# start_kb3.row(KeyboardButton(text="Залишіть відгук")) # Додаємо кнопку "Залишіть відгук" в кінець клавіатури