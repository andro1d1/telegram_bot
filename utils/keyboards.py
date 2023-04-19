from aiogram import types

main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
buttons_main_menu = [
    types.KeyboardButton(text="Текущая погода", callback_data="weather"),
    types.KeyboardButton(text="Конвертация валюты",
    callback_data="exchange_rates"),
    types.KeyboardButton(text="Картинка ¯\_(ツ)_/¯", callback_data="picture"),
    types.KeyboardButton(text="Текущий квиз", callback_data="quiz")
]
main_menu.add(*buttons_main_menu)
