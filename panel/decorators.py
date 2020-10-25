from datetime import date
from functools import wraps

from django.shortcuts import redirect, reverse

from .models import Profile


def whether_profile_set(view_func):
    @wraps(view_func)
    def _actual_decorator(request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        if profile.date_of_birth == date(year=1410, day=15, month=9) or profile.sex is None:
            return redirect(reverse("settings"))

        return view_func(request, *args, **kwargs)

    return _actual_decorator
