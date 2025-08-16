import os
"""Calculate the final price for a shopping cart.

Rules:
- VIP customers get a 20% discount.
- Shipping is free if the cart value exceeds 200 PLN.
  Otherwise: 15 PLN for 'courier', 10 PLN for 'pickup'.
- For non-VIP customers with small carts, no discount applies.

Returns:
    tuple: (total_price, description) where description is a formatted string
           with total, discount, and shipping costs.
"""
path = os.path.dirname(os.path.realpath(__file__))
os.system(f'flake8 {path}/item7-9.py')


def calculate_price_v1(cart_value: float, is_vip: bool, shipping_method: str):
    total_price = cart_value

    if not isinstance(cart_value, float) and not isinstance(cart_value, int):
        raise TypeError('Cart value must be the float or int!')
    elif not isinstance(is_vip, bool):
        raise TypeError('is_vip must be boolean!')
    elif not isinstance(shipping_method, str):
        raise TypeError('Shipping method must be a string!')

    if cart_value <= 0:
        raise ValueError('Make sure that the cart value is correct.')

    if shipping_method not in ['pickup', 'courier']:
        raise ValueError('Choose the correct shipping method')

    if is_vip:
        total_price *= 0.8

    if cart_value < 200 and shipping_method == 'pickup':
        shipping_cost = 10
    elif cart_value < 200 and shipping_method == 'courier':
        shipping_cost = 15
    else:
        shipping_cost = 0

    total_price += shipping_cost

    print(f'You have to pay {total_price:.2f} PLN (discount: '
          + f'{cart_value*0.2:.2f} PLN, shipping: {shipping_cost:.2f} PLN)')


def calculate_price_v2(cart_value: float, is_vip: bool, shipping_method: str):

    if not isinstance(cart_value, float) and not isinstance(cart_value, int):
        raise TypeError('Cart value must be the float or int!')
    elif not isinstance(is_vip, bool):
        raise TypeError('is_vip must be boolean!')
    elif not isinstance(shipping_method, str):
        raise TypeError('Shipping method must be a string!')

    if cart_value <= 0:
        raise ValueError('Make sure that the cart value is correct.')

    if shipping_method not in ['pickup', 'courier']:
        raise ValueError('Choose the correct shipping method')

    discount = (cart_value*0.2) if is_vip else 0

    shipping_cost = (0 if cart_value >= 200
                     else (15 if shipping_method == 'courier' else 10))

    total_price = cart_value - discount + shipping_cost

    print(f'You have to pay {total_price:.2f} PLN (discount: '
          + f'{discount:.2f} PLN, shipping: {shipping_cost:.2f} PLN)')


calculate_price_v1(199, True, 'pickup')

calculate_price_v2(200, False, 'courier')
