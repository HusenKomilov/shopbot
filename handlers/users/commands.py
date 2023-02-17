'''KOMANDALARNI ILADIGAN HANDLERLAR'''

from telebot.types import Message
from data.loader import bot, db
from keyboards.default import main_menu


@bot.message_handler(commands=['start'], chat_types='private')
def start(message: Message):
    chat_id = message.chat.id
    db.insert_telegram_id(chat_id)
    first_name = message.from_user.first_name
    bot.send_message(chat_id, f"Salom, {first_name}", reply_markup=main_menu())
    # bot.copy_message(2131715946, chat_id, f"{message.message_id}", caption=f"{first_name}")
    # bot.forward_message(2131715946, chat_id, message.message_id)
