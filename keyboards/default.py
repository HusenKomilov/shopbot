'''
SIZ BU YERDA ODDIY KNOPKALAR YARATA OLASIZ
'''

from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    catalog = KeyboardButton('Katalog ๐')
    feedback = KeyboardButton('Bog\'lanish uchun ๐')
    settings = KeyboardButton('Sozlamalar โ')

    markup.add(catalog, feedback, settings)

    return markup

def register_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    register = KeyboardButton("Ro'yxatdan o'tish ๐งพ")

    markup.add(register)
    return markup

def save_contact():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    contact = KeyboardButton('Kontactni ulashish', request_contact=True)

    markup.add(contact)
    return markup