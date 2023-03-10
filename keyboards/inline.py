'''
SIZ BU YERDA INLINE KNOPKALAR YARATA OLASIZ
'''
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from data.loader import db


def get_categories_buttons(category_list):
    markup = InlineKeyboardMarkup(row_width=1)
    for item in category_list:
        category_name = item[0]
        category_id = db.select_category_by_cat_name(category_name)[0]
        name = ''
        if category_name == 'phones':
            name = 'Telefonlar'
        elif category_name == 'tv':
            name = 'Televizorlarga'
        elif category_name == 'air-conditioners':
            name = 'Konditsionerlar'
        elif category_name == 'stiralniye-mashini':
            name = 'Kir yuvish mashinalari'
        btn = InlineKeyboardButton(name, callback_data=f'category|{category_id}')
        markup.add(btn)
    asd = InlineKeyboardButton('Orqaga', callback_data='main_menu')
    markup.add(asd)
    return markup


def get_products_list_buttons(product_list):
    markup = InlineKeyboardMarkup()
    for item in product_list:
        btn = InlineKeyboardButton(item[0], callback_data=f"product|{item[1]}")
        markup.add(btn)
    back = InlineKeyboardButton('Orqaga🔙', callback_data='back_categories')
    markup.add(back)
    return markup


def get_products_by_pagination(category_id, page=1):
    markup = InlineKeyboardMarkup()
    limit = 6
    offset = (page - 1) * limit

    products = db.select_products_by_paginations(category_id, offset, limit)

    for product in products:
        markup.add(InlineKeyboardButton(product[0], callback_data=f"product|{product[1]}"))

    count = db.count_products_by_category_id(category_id)
    max_page = count // limit if count % limit == 0 else count % limit + 1

    back = InlineKeyboardButton('⏮', callback_data=f"previous_page|{category_id}")
    currnet_page = InlineKeyboardButton(f"{page}", callback_data="current_page")
    next = InlineKeyboardButton('⏭', callback_data=f'next_page|{category_id}')

    if 1 < page < max_page:
        markup.add(back, currnet_page, next)
    elif page == 1:
        markup.add(currnet_page, next)
    else:
        markup.add(back, currnet_page)

    markup.add(
        InlineKeyboardButton('Orqaga', callback_data='back_categories'),
        InlineKeyboardButton('Bosh menuga', callback_data='main_menu')
    )
    return markup


def get_product_control_buttons(category_id, product_id, quantity=1):
    quantity_btn = [
        InlineKeyboardButton("➖", callback_data="minus"),
        InlineKeyboardButton(quantity, callback_data="quantity"),
        InlineKeyboardButton("➕", callback_data="plus")
    ]

    card = [
        InlineKeyboardButton("Savatga qo'shish", callback_data=f"add|{product_id}"),
        InlineKeyboardButton("Savat 🛒", callback_data="show_card")
    ]

    backs = [
        InlineKeyboardButton("Ortga 🔙", callback_data=f"category|{category_id}"),
        InlineKeyboardButton("Katalg 📇", callback_data=f"back_categories")
    ]

    main_menu = [
        InlineKeyboardButton("Asosiy sahifa", callback_data="main_menu")
    ]

    return InlineKeyboardMarkup(keyboard=[quantity_btn, card, backs, main_menu])


def show_card_buttons(data: dict):
    markup = InlineKeyboardMarkup(row_width=1)

    for product_name, item in data.items():
        product_id = item['product_id']
        btn = InlineKeyboardButton(f"❌{product_name}", callback_data=f'remove|{product_id}')
        markup.add(btn)
    back = InlineKeyboardButton("Katalg 📇", callback_data=f"back_categories")
    clear = InlineKeyboardButton("Tozalash 🔄", callback_data='clear_card')
    order = InlineKeyboardButton("Buyurtmani tasdiqlash✅", callback_data=f"submit")
    markup.row(clear, order)
    markup.row(back)
    return markup
