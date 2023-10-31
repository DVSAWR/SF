from django import template

import re

register = template.Library()

censor_list = ['lorem', 'non', 'sit', 'but']

def repl_censor(value):
    word = value.group()
    if word.lower() in censor_list:
        return word[0] + '*' * (len(word) - 1)
    else:
        return word


@register.filter()
def censor(value):
    if str != type(value):
        raise TypeError('CUSTOM ERROR: VALUE TYPE ERROR IN DEF CENSOR')

    value = re.sub(r'\b\w*\b', repl_censor, value, flags=re.I|re.U)

    return value


