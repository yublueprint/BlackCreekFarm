from django import template

register = template.Library()


@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, None)


@register.filter
def has_attr(obj, attr_name):
    return hasattr(obj, attr_name)
