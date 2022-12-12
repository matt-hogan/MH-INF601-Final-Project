from django import template

register = template.Library()

@register.simple_tag
def add_plus(odd):
    """ Adds a plus sign in front of positive numbers to be rendered in HTML """
    if odd and odd > 0:
        return f"+{odd}"
    return f"{odd}"