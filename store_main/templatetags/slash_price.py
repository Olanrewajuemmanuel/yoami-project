from django import template

register = template.Library()

@register.filter
def slash_price(value, discount):
    if discount:
        new_price =  value * discount / 100
        return round(new_price, 2)
    else:
        return value


