'''
BOTNI ISHGA TUSHIRISH
'''
from middlewares import SimpleMiddleware
from data.loader import bot, db
from product_pars import OpenShopParser

import handlers


def create_tables(database, pars_opp):
    database.create_categories_table()
    database.create_products_table()
    database.create_users_table()

    database.insert_categories('phones')
    database.insert_categories('tv')
    database.insert_categories('air-conditioners')
    database.insert_categories('stiralniye-mashini')

    product_list = [pars_opp('phones').get_info(),
                    pars_opp('tv').get_info(),
                    pars_opp('air-conditioners').get_info(),
                    pars_opp('stiralniye-mashini').get_info()]
    print(product_list)

    # for item in product_list:
    #     for product_item in item:
    #         cat_id = product_item['category_id']
    #         name = product_item['title']
    #         image = product_item['image']
    #         link = product_item['link']
    #         price = product_item['price']

    #         database.insert_products(name, link, price, image, cat_id)


bot.setup_middleware(SimpleMiddleware(1))  # bu botga qayta qayta yozmaslik uchun limit(sekundda) kiritiladi

if __name__ == '__main__':
    create_tables(db, OpenShopParser)
    bot.infinity_polling()
