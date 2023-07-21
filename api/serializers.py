from rest_framework import serializers
from django.contrib.auth.models import User

from api.models import HealthMeasurement


class HealthMeasurementSerializer(serializers.ModelSerializer):


    class Meta:
        model = HealthMeasurement
        fields = ['type', 'unit', 'value',  'startDate', 'endDate', 'metadata']

class AllHealthMeasurementSerializer(serializers.ModelSerializer):


    class Meta:
        model = HealthMeasurement
        fields = '__all__'
