from django.contrib.auth.models import User

from django.db import models

class HealthMeasurement(models.Model):

    MEASUREMENT_TYPES = (
        ('HeartRate', 'HeartRate'),
        ('StepCount', 'StepCount'),
        ('SleepAnalysis', 'SleepAnalysis'),
        ('BloodGlucose', 'BloodGlucose'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=MEASUREMENT_TYPES)
    unit = models.CharField(max_length=20)
    value = models.FloatField()
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    metadata = models.JSONField()

    def __str__(self) -> str:
        return f'{self.user}\'s {self.type} data from {self.startDate} to {self.endDate}'
