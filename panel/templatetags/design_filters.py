from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def none_to_dash(text):
    if text == None:
        return mark_safe("---")
    return text


@register.filter
def is_logged_formula(user):
    if user.is_authenticated:
        return mark_safe(
            "<a class='a-yellow a-margin' href={}>Wyloguj się</a>".format(reverse("logout"))
        )
    else:
        return mark_safe(
            "<a class='a-yellow a-margin' href={}>Zaloguj się</a><a class='a-yellow a-margin' href={}>Zarejestruj się</a>".format(
                reverse("login"), reverse("register"))
        )


@register.filter
def bmi_class(bmi):
    if type(bmi) == str:
        return "border-primary text-primary-important"
    elif bmi > 29.99 or bmi < 17:
        return "bg-danger"
    elif bmi > 24.99 or bmi < 18.5:
        return "bg-warning"
    else:
        return "bg-success"


@register.filter
def bmi_description(bmi):
    if bmi > 39.99:
        return "III stopień otyłości (otyłość skrajna)"
    if type(bmi) == str:
        return "---"
    elif bmi > 39.99:
        return "III stopień otyłości(otyłość skrajna)"
    elif bmi > 34.99:
        return "II stopień otyłości (otyłość kliniczna)"
    elif bmi > 29.99:
        return "I stopień otyłości"
    elif bmi > 24.99:
        return "nadwagę"
    elif bmi < 16:
        return "wygłodzenie"
    elif bmi < 17:
        return "wychudzenie"
    elif bmi < 18.5:
        return "niedowagę"
    else:
        return "prawidłową wartość"
