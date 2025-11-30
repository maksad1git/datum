from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Template filter to get dictionary item by key.

    Usage: {{ mydict|get_item:mykey }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key, '')


@register.filter
def add_str(value1, value2):
    """
    Concatenate two strings.

    Usage: {{ "attr_"|add_str:attr.id }}
    """
    return str(value1) + str(value2)
