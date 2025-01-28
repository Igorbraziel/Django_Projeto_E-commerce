from django.template import Library

register = Library()

@register.filter
def price_format(value):
    return f'R$ {value:.2f}'