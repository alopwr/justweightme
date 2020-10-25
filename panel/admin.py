# Register your models here.
from django.contrib import admin

from .models import Profile, Measurement

# Register your models here.

admin.site.register(Profile)
admin.site.register(Measurement)
