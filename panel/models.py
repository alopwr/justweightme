from datetime import date

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    height = models.IntegerField(blank=True, default=0, verbose_name="Wzrost")
    date_of_birth = models.DateField(blank=True, verbose_name="Data urodzenia")
    sex = models.CharField(null=True, blank=False, max_length=1, choices=(('M', 'mężczyzna'), ('F', 'kobieta')),
                           verbose_name="płeć")
    chart_js_code = models.TextField(null=True)
    goal_weight = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)], verbose_name="")

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    @property
    def goal(self):
        if self.goal_weight:
            return self.goal_weight
        return self.ideal_weight

    @property
    def ideal_weight(self):
        # Lorentz's algorithm
        if self.sex == 'kobieta':
            return self.height - 100 - ((self.height - 150) / 2)
        return self.height - 100 - ((self.height - 150) / 4)

    def __str__(self):
        return 'Profil użytkownika {}'.format(self.user.username)


class Measurement(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='measurements')
    weight = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)], verbose_name="Masa ciała")
    bf_percent = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)],
                                   verbose_name="Procent tkanki tłuszczowej")
    created_at = models.DateTimeField(auto_now=True)

    @property
    def bmi(self):
        try:
            return round(self.weight / ((self.profile.height / 100) ** 2), 2)
        except (ZeroDivisionError, TypeError):
            return "---"

    def __str__(self):
        return "Pomiar z {}".format(timezone.localtime(self.created_at).strftime('%H:%M %d.%m.%y'))


class Signature(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    signature = models.IntegerField(default=0)
