from django import template

register = template.Library()

def get_val(dict, key):
    return dict.get(key)
register.filter('get_val', get_val)