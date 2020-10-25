from django import template

register = template.Library()


@register.filter
def exclude(list, exlud):
    new_list = []

    for field in list:
        if field.name not in exlud:
            new_list.append(field)

    return new_list
