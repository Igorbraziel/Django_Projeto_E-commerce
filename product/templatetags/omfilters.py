from django.template import Library
from utils import my_functions

register = Library()

@register.filter
def price_format(value):
    return my_functions.price_format(value)

@register.filter
def cart_total_quantity(cart):
    return my_functions.cart_total_quantity(cart)

@register.filter
def cart_total_value(cart):
    return my_functions.cart_total_value(cart)