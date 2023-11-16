from django import template

register = template.Library()


@register.filter()
def censor(value):
    censored = ['lorem', 'non', 'sit', 'but']
    words = value.split()
    for i in range(len(words)):
        if words[i] in censored:
            words[i] = words[i][0] + '*' * (len(words[i]) - 1)

    return ' '.join(words)