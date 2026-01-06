"""
Custom template tags and filters for the planning app.
"""

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary using a variable key.
    
    Usage: {{ mydict|get_item:key_var }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def flatten_list(dict_values):
    """
    Flatten a dict_values into a single list.
    
    Usage: {{ events_by_day.values|flatten_list }}
    """
    result = []
    for item_list in dict_values:
        result.extend(item_list)
    return result
