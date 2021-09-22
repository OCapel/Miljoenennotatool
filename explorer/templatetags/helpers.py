import re

from django import template

register = template.Library()


@register.filter(name='highlight')
def highlight(data, query):
    terms = query.split(' OR ')
    for term in terms:
        pattern = re.compile(term, re.IGNORECASE)
        data = pattern.sub(r'<em class="highlight">\g<0></em>', data)
    return data

@register.filter(name='lookup')
def lookup(dict, index):
    if index in dict:
        return dict[index]
    return ''

