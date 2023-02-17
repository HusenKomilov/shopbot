'''TEXTLARNI ILADIGAN HANDLERLAR'''
from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db
from keyboards.default import main_menu, register_button, save_contact
from keyboards.inline import get_categories_buttons


@bot.message_handler(func=lambda message: message.text == "Katalog 📇")
def catalog(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    check = db.check_user_for_registration(from_user_id)

    if None in check:
        text = "Siz ro'yxatdan o'tmagansiz. Iltimos ro'yxatdan o'ting."
        markup = register_button()
    else:
        bot.delete_message(chat_id, message.message_id)
        text = 'Katalog'
        categories_list = db.select_category_name()
        markup = get_categories_buttons(categories_list)

    bot.send_message(chat_id, "Quyidagi boplimlardan birini tanlang👇", reply_markup=ReplyKeyboardRemove())
    bot.delete_message(chat_id, message.message_id + 1)
    bot.send_message(chat_id, text, reply_markup=markup)


data = {}


@bot.message_handler(regexp="Ro'yxatdan o'tish 🧾")
def register(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    msg = bot.send_message(chat_id, 'Ism va familiyangizni kiriting.\n\
        Namuna 👇\n\
        Komilov Huseyn', reply_markup=ReplyKeyboardRemove())

    bot.register_next_step_handler(msg, save_name)


def save_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    full_name = message.text.title()

    data[from_user_id] = {'full_name': full_name}

    msg = bot.send_message(chat_id, 'Telefon raqamni kiritng:', reply_markup=save_contact())

    bot.register_next_step_handler(msg, save_phone)


def save_phone(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    contact = message.contact.phone_number

    data[from_user_id]['contact'] = contact
    msg = bot.send_message(chat_id, "Tug'ilgan kuningizni <b>yyyy.mm.dd</b> ko'rinishida kiriting.",
                           reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, user_save)


def user_save(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    birth_date = message.text
    data[from_user_id]['birth_date'] = birth_date
    full_name = data[from_user_id]['full_name']
    contact = data[from_user_id]['contact']

    db.user_save(full_name, contact, birth_date, from_user_id)
    categories_list = db.select_category_name()
    markup = get_categories_buttons(categories_list)
    bot.send_message(chat_id, "Tabriklayman siz ro'yxatdan o'tdingiz.", reply_markup=markup)


