from django.template import Library

register = Library()

@register.filter
def price_format(value):
    return f'R$ {value:.2f}'

@register.filter
def cart_total_quantity(cart):
    return sum([cart_element['quantity'] for cart_element in cart.values()])

@register.filter
def cart_total_value(cart):
    total_value = 0
    for cart_element in cart.values():
        if cart_element['quantitative_promotional_price']:
            total_value += cart_element['quantitative_promotional_price']
        else:
            total_value += cart_element['quantitative_price']
    return total_value