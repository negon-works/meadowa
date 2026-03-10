from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0  # Default to 0 if there's an error
