from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from panel.api.serializers import MeasurementSerializer, ProfileSerializer, SignatureSerializer
from panel.models import Measurement, Profile, Signature


class MeasurementViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        return Measurement.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)


class SignatureViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SignatureSerializer

    def get_queryset(self):
        return Signature.objects.filter(user=self.request.user)
