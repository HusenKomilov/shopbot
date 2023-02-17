from .shipping_product import Product
from telebot.types import LabeledPrice, ShippingOption


def generate_product_invoice(product_data):
    query = Product(
        title="ShopBot",
        description="\n".join(title for title in product_data),
        currency='UZS',
        prices=[LabeledPrice(
            label=f"{product_data[title]['quantity']} ta {title}",
            amount=int(product_data[title]['quantity'] * int(product_data[title]['price']) * 100)
        ) for title in product_data],
        start_parameter='create_invoice_products',
        need_name=True,
        need_phone_number=True,
        is_flexible=True
    )
    return query


EXPRESS_SHIPPING = ShippingOption(
    id="post_express",
    title='1-kun ichida'
).add_price(LabeledPrice("1-kun ichida yetkazib berish", 2500000))

REGULAR_SHIPPING = ShippingOption(
    id='post_regular',
    title='3-kun ichida'
).add_price(LabeledPrice('3-kun ichida yetkazib berish', 1500000))

PICKUP_SHIPPING = ShippingOption(
    id='post_pickup',
    title="Do'kondan olib ketish"
).add_price(LabeledPrice("Do'kondan olib ketish", 0))

REGION_SHIPPING = ShippingOption(
    id='post_region',
    title="O'zbekiston bo'ylab"
).add_price(LabeledPrice("O'zbekiston bo'ylab yetkazish", 10000000))