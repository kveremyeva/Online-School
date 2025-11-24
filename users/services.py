import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(content_object):
    product = stripe.Product.create(
        name=content_object.name,
        type='service'
    )

    return product.id


def create_stripe_price(amount, product_id):
    """Создание цены в Stripe для существующего продукта"""
    price = stripe.Price.create(
        unit_amount=int(amount * 100),
        currency='rub',
        product=product_id,
    )
    return price


def create_stripe_session(price):
    """ Создает сессию на оплату в страйпе"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        payment_method_types=['card'],
        line_items=[{
            "price": price.id,
            "quantity": 1,
        }],
        mode="payment"
    )
    return session.id, session.url
