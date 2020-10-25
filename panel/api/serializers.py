from rest_framework import serializers

from ..models import Measurement, Profile, Signature


class MeasurementSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField()
    profile = serializers.ReadOnlyField(source='profile.user.name')

    class Meta:
        model = Measurement
        fields = '__all__'
        write_only_fields = 'profile'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('chart_js_code', 'user', 'id')


class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        fields = ('signature',)
