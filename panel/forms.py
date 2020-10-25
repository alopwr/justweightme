from datetime import date
from math import sqrt

from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .models import Profile, Measurement


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('height', 'sex', 'date_of_birth', 'goal_weight')
        widgets = {
            'date_of_birth': DatePickerInput(format='%Y-%m-%d'),
        }

    def clean_date_of_birth(self):
        value = self.cleaned_data.get("date_of_birth")
        today = date.today()
        age = today.year - value.year - (
                (today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise ValidationError("Musisz mieć co najmniej 18 lat.")
        elif age > 200:
            raise ValidationError("I tak ci nie uwierzymy, że masz tyle lat :)")

        return value


class ChartsForm(forms.Form):
    chart_type = forms.ChoiceField(choices=(
        (7, "tydzień"), (14, "dwa tygodnie"), (31, "miesiąc"), (62, "dwa miesiące"),
        (183, "sześć miesięcy"), (365, "rok"), ("inny", "inny okres czasu")), label="", initial=14, )
    different = forms.IntegerField(label="", widget=forms.NumberInput(
        attrs={"placeholder": "Podaj dokładną liczbę dni do generacji", "style": "display:none;"}),
                                   required=False, validators=[MinValueValidator(1)])


class MenMeasurementForm(forms.ModelForm):
    thigh = forms.FloatField(validators=[MinValueValidator(0)], required=False, label="Udo")
    pectoral = forms.FloatField(validators=[MinValueValidator(0)], required=False, label="Klatka piersiowa")
    abdominal = forms.FloatField(validators=[MinValueValidator(0)], required=False, label="Brzuch")

    class Meta:
        model = Measurement
        fields = ("weight", "bf_percent")

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.profile = self.request.user.profile
        instance = self.jackson_pallock(instance)
        if commit:
            instance.save()
        return instance

    def jackson_pallock(self, instance):
        if self.cleaned_data.get("weight", False) and self.cleaned_data.get("thigh", False) and self.cleaned_data.get(
                "pectoral", False) and self.cleaned_data.get("abdominal", False):
            summ = self.cleaned_data.get("thigh", 0) + self.cleaned_data.get("pectoral", 0) + self.cleaned_data.get(
                "abdominal", 0)
            age = self.request.user.profile.age
            body_density = 1.10938 - (0.0008267 * summ) + (0.0000016 * sqrt(summ)) - (0.0002574 * age)
            fat = (495 / body_density) - 450
            instance.bf_percent = round(fat, 2)

        return instance


class FemaleMeasurementForm(MenMeasurementForm):
    tricep = forms.FloatField(validators=[MinValueValidator(0)], required=False, label="Triceps")
    suprailiac = forms.FloatField(validators=[MinValueValidator(0)], required=False, label="Skos brzucha")
    pectoral = None
    abdominal = None

    def jackson_pallock(self, instance):
        if self.cleaned_data.get("weight", False) and self.cleaned_data.get("thigh", False) and self.cleaned_data.get(
                "tricep", False) and self.cleaned_data.get("suprailiac", False):
            summ = self.cleaned_data.get("thigh", 0) + self.cleaned_data.get("tricep", 0) + self.cleaned_data.get(
                "suprailiac", 0)
            age = self.request.user.profile.age
            body_density = 1.0994921 - (0.0009929 * summ) + (0.0000023 * sqrt(summ)) - (0.0001392 * age)
            fat = (495 / body_density) - 450
            instance.bf_percent = round(fat, 2)

        return instance
