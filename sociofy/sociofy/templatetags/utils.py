from django import template

register = template.Library()

@register.filter
def type_of(value):
    return type(value).__name__
