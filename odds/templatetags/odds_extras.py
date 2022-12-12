from django import template

register = template.Library()

@register.simple_tag
def add_plus(odd):
    if odd and odd > 0:
        return f"+{odd}"
    return f"{odd}"