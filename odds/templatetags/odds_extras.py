from django import template

register = template.Library()

@register.simple_tag
def add_plus(odd):
    try:
        if odd > 0:
            return f"+{odd}"
    except Exception as exc:
        pass
    return f"{odd}"