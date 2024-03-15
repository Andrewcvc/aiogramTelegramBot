from aiogram.types import BotCommand

private_commands = [
    BotCommand(command="menu", description="Меню"),
    BotCommand(command="about", description="Інформацію про бота"),
    BotCommand(command="payment", description="Варіанти оплати"),
    BotCommand(command="shipping", description="Способи доставки")
]