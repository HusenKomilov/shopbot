'''CALLBACKLARNI ILADIGAN HANDLERLAR'''
from telebot.types import CallbackQuery
from data.loader import bot, db
from keyboards.default import main_menu
from keyboards.inline import get_categories_buttons, get_products_by_pagination, get_product_control_buttons, \
    show_card_buttons
from states.states import CardState
from shipping_data.shipping_detail import generate_product_invoice
from config import ADMINS


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def nazad(call: CallbackQuery):
    chat_id = call.message.chat.id
    text = 'Bosh sahifa'
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text, reply_markup=main_menu())


@bot.callback_query_handler(func=lambda call: 'category|' in call.data)
def reaction_to_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    category_id = call.data.split('|')[1]
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, 'Mahsulotlar', reply_markup=get_products_by_pagination(category_id))


@bot.callback_query_handler(func=lambda call: call.data == 'back_categories')
def reaction_back_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    categories_list = db.select_category_name()
    text = 'Katalog'
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text, reply_markup=get_categories_buttons(categories_list))


@bot.callback_query_handler(func=lambda call: 'next_page|' in call.data)
def reaction_to_next_page(call: CallbackQuery):
    chat_id = call.message.chat.id

    page = 0
    elements = call.message.reply_markup.keyboard[-2]
    category_id = int(call.data.split('|')[1])

    for element in elements:
        if element.callback_data == 'current_page':
            page = int(element.text)

    page += 1

    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, 'Mahsulotlar', reply_markup=get_products_by_pagination(category_id, page))


@bot.callback_query_handler(func=lambda call: 'previous_page|' in call.data)
def reaction_to_previous_page(call: CallbackQuery):
    chat_id = call.message.chat.id

    elements = call.message.reply_markup.keyboard[-2]
    category_id = int(call.data.split('|')[1])

    page = None

    for element in elements:
        if element.callback_data == 'current_page':
            page = int(element.text)
    page -= 1
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, 'Mahsulotlar', reply_markup=get_products_by_pagination(category_id, page))


@bot.callback_query_handler(func=lambda call: call.data == 'current_page')
def reaction_to_current_page(call: CallbackQuery):
    elements = call.message.reply_markup.keyboard[-2]

    for element in elements:
        if element.callback_data == 'current_page':
            page = int(element.text)

    bot.answer_callback_query(call.id, f"Siz {page}-sahifadasiz", show_alert=True)


@bot.callback_query_handler(func=lambda call: 'product|' in call.data)
def reaction_to_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    product_id = call.data.split('|')[1]

    product = db.select_product_by_id_all(product_id)
    title, link, price, image, cat_id = product

    bot.delete_message(chat_id, call.message.message_id)
    bot.send_photo(chat_id, image,
                   caption=f"<b>{title}</b>\n Narxi <i>{price}</i>\n <a href='{link}'>Batafsil ma'lumot</a>",
                   reply_markup=get_product_control_buttons(cat_id, product_id))


@bot.callback_query_handler(func=lambda call: call.data in ['plus', 'minus'])
def reaction_to_plus_minus(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id, cache_time=1)

    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    category_id = call.message.reply_markup.keyboard[2][0].callback_data.split('|')[1]
    product_id = call.message.reply_markup.keyboard[1][0].callback_data.split('|')[1]

    if call.data == 'plus':
        quantity += 1
    elif call.data == 'minus':
        if quantity > 1:
            quantity -= 1
    try:
        bot.edit_message_reply_markup(chat_id, call.message.id,
                                      reply_markup=get_product_control_buttons(category_id, product_id, quantity))
    except:
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'quantity')
def quantity(call: CallbackQuery):
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    bot.answer_callback_query(call.id, f"Siz {quantity} ta mahsulot tanladingiz", show_alert=True, cache_time=1)


@bot.callback_query_handler(func=lambda call: 'add|' in call.data)
def reaction_to_add(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    product_id = int(call.data.split('|')[1])
    product = db.select_product_by_id_all(product_id)
    product_name = product[0]
    product_price = product[2]
    quantity = int(call.message.reply_markup.keyboard[0][1].text)
    bot.set_state(from_user_id, CardState.card, chat_id)
    bot.answer_callback_query(call.id, text="Savatga qo'shildi", cache_time=1)

    with bot.retrieve_data(from_user_id, chat_id) as data:
        if data.get('card'):
            data['card'][product_name] = {
                'product_id': product_id,
                'price': product_price,
                'quantity': quantity
            }
        else:
            data['card'] = {
                product_name: {
                    'product_id': product_id,
                    'price': product_price,
                    'quantity': quantity
                }
            }


@bot.callback_query_handler(func=lambda call: call.data == 'show_card')
def reaction_show_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id

    try:
        with bot.retrieve_data(from_user_id, chat_id) as data:
            result = get_text_reply_markup(data)
        text = result['text']
        markup = result['markup']
        total_price = result['total_price']
        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id, text, reply_markup=markup)
    except:
        bot.answer_callback_query(call.id, text='Siz hozircha hech qanday mahsulot tanlamadingiz!', show_alert=True)


@bot.callback_query_handler(func=lambda call: 'remove|' in call.data)
def reaction_remove_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    product_id = int(call.data.split('|')[1])

    with bot.retrieve_data(from_user_id, chat_id) as data:
        keys = [product_name for product_name in data['card'].keys()]

        for key in keys:
            if data['card'][key]['product_id'] == product_id:
                del data['card'][key]

    result = get_text_reply_markup(data)
    text = result['text']
    markup = result['markup']
    total_price = result['total_price']
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, text, reply_markup=markup)


def get_text_reply_markup(data):
    text = 'Savat: \n'
    total_price = 0

    for product_name, item in data['card'].items():
        product_price = item['price']
        quantity = item['quantity']
        price = quantity * product_price
        total_price += price
        text += f"{product_name}\n Narxi: {quantity} * {product_price} = {price}\n"

    if total_price == 0:
        text += "Savatingiz bo'sh"
        markup = main_menu()
    else:
        text += f"Umumiy narx {total_price}"
        markup = show_card_buttons(data['card'])

    return {'text': text, 'markup': markup, 'total_price': total_price}


@bot.callback_query_handler(func=lambda call: call.data == 'clear_card')
def reaction_to_clear_card(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    category_list = db.select_category_name()
    bot.delete_state(from_user_id, chat_id)
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, 'Mahsulotlar', reply_markup=get_categories_buttons(category_list))


@bot.callback_query_handler(func=lambda call: call.data == 'submit')
def reaction_to_submit(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id

    bot.delete_message(chat_id, call.message.message_id)
    name = call.message.chat.first_name

    with bot.retrieve_data(from_user_id, chat_id) as data:
        bot.send_invoice(chat_id, **generate_product_invoice(data['card']).generate_invoice(),
                         invoice_payload='shop_bot')
