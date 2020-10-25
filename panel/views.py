from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView

from .charts import generate_chart
from .forms import ProfileForm, ChartsForm, MenMeasurementForm, FemaleMeasurementForm
from .models import Measurement, Profile


class DashboardView(ListView):
    model = Measurement
    template_name = "panel/dashboard_view.html"

    def get_queryset(self):
        profile = self.request.user.profile
        return self.model.objects.filter(profile=profile).order_by("-created_at")


class NewMeasurementView(CreateView):
    template_name = "panel/new_measurement.html"
    success_url = reverse_lazy("dashboard")

    def get_form_class(self, form_class=None):
        if self.request.user.profile.sex == "M":
            return MenMeasurementForm
        else:
            return FemaleMeasurementForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class DeleteMeasurementView(DeleteView):
    model = Measurement
    success_url = reverse_lazy("dashboard")
    template_name = "panel/delete_measurement.html"


class SettingsView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "panel/settings.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        return self.request.user.profile


class DetailMeasurementView(DetailView):
    model = Measurement
    template_name = "panel/detail.html"

    def get(self, *args, **kwargs):
        if not self.get_object().profile.user.id == self.request.user.id:
            raise PermissionDenied
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Measurement.objects.filter(profile__user=self.request.user).order_by("-created_at")
        return context


class ChartsView(FormView):
    form_class = ChartsForm
    template_name = "panel/charts_view.html"
    chart_type = 14

    def get_context_data(self, **kwargs):
        contex = super().get_context_data()

        if self.chart_type == 14:
            contex["chart_js_code"] = self.profile.chart_js_code
        else:
            contex["chart_js_code"] = generate_chart(self.profile, self.chart_type)

        return contex

    def get(self, request, *args, **kwargs):
        self.profile = self.request.user.profile
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            try:
                self.chart_type = int(form.cleaned_data["chart_type"])
            except ValueError:
                self.chart_type = int(form.cleaned_data["different"])

        return self.get(request, *args, **kwargs)


def get_if_generated(request):
    profile = request.user.profile
    if profile.chart_js_code == 'spinner':
        done = False
    else:
        done = True

    return JsonResponse({'done': done, })
