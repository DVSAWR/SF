import re
from django import template

register = template.Library()

censor_list = ['aldus', 'pagemaker']


def pre_censor(value):
    word = value.group()
    if word.lower() in censor_list:
        return word[0] + '*' * (len(word)-1)
    else:
        return word


@register.filter()
def censor(value):
    if str != type(value):
        raise TypeError('VALUE TYPE ERROR IN DEF CENSOR')

    value = re.sub(r'\b\w*\b', pre_censor, value, flags=re.I | re.U)

    return value
