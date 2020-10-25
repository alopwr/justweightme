"""slimmerme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from panel import views
from .decorators import whether_profile_set

urlpatterns = [
    path('', login_required(whether_profile_set(views.DashboardView.as_view())), name='dashboard'),
    path('measurements/new', login_required(whether_profile_set(views.NewMeasurementView.as_view())), name='new'),
    path('measurements/<slug:pk>/delete', login_required(whether_profile_set(views.DeleteMeasurementView.as_view())),
         name='delete'),
    path('settings', login_required(views.SettingsView.as_view()), name='settings'),
    path('charts', login_required(whether_profile_set(views.ChartsView.as_view())), name='charts'),
    path('measurements/<slug:pk>/', login_required(whether_profile_set(views.DetailMeasurementView.as_view())),
         name='detail'),
    path('instruction/',
         login_required(whether_profile_set(TemplateView.as_view(template_name="panel/instruction.html"))),
         name='instruction'),
    path('ajax-generating-done/', views.get_if_generated, name="ajax-charts"),
]
