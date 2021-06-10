from django import template

register = template.Library()


@register.filter
def round_by_two(value):
    return round(value, 2)
