from datetime import date, timedelta

import decouple
import requests
from django.contrib.auth import login
from django.shortcuts import render, redirect, reverse

from account.forms import UserRegistrationForm
from panel.models import Profile, Signature


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse("dashboard"))
    if request.method == 'POST':
        user_form = UserRegistrationForm(data=request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            signature = Signature.objects.create(user=new_user)
            profile = Profile.objects.create(user=new_user,
                                             date_of_birth=(date.today() - timedelta(days=6574)))  # 18 years
            add_sendgrid_contact(new_user.email, decouple.config("SENDGRID_LIST_ID"))
            login(request, new_user)
            return redirect(reverse("settings"))
    else:
        user_form = UserRegistrationForm
    return render(request, 'account/register.html', {'user_form': user_form})


def add_sendgrid_contact(email, list_id):
    headers = {
        'authorization': 'Bearer {}'.format(decouple.config("SENDGRID_API_KEY")),
        'content-type': 'application/json',
    }

    data = '{"list_ids":["' + list_id + '"],"contacts":[{"email":"' + email + '"}]}'
    response = requests.put('https://api.sendgrid.com/v3/marketing/contacts', headers=headers, data=data)
