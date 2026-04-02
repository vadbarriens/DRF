import stripe
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(name):
    """Create product in the stripe"""
    product = stripe.Product.create(name=name)
    return product


def create_stripe_price(amount, product):
    """Create price in the stripe"""
    price = stripe.Price.create(
        product=product.get('id'),
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": "Payment_price"},
    )
    return price


def create_stripe_session(price):
    """Create session in the stripe"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:800/",
        line_items=[{"price": price.get('id'), "quantity": 1}],
        mode="payment",
    )
    return session.get('id'), session.get('url')
