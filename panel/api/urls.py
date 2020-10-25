from django.urls import path, include
from rest_framework import routers

from panel.api import views

router = routers.DefaultRouter()
router.register('measurements', views.MeasurementViewSet, basename='Measurement')
router.register('profile', views.ProfileViewSet, basename='Profile')
router.register('signature', views.SignatureViewSet, basename='Signature'),

urlpatterns = [
    path('', include(router.urls)),
]
