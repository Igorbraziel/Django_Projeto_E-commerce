def price_format(value):
    return f'R$ {value:.2f}'

def cart_total_quantity(cart):
    return sum([cart_element['quantity'] for cart_element in cart.values()])

def cart_total_value(cart):
    return sum(
        [
            cart_element.get('quantitative_promotional_price')
            if cart_element.get('quantitative_promotional_price')
            else cart_element.get('quantitative_price')
            for cart_element in cart.values()
        ]
    )