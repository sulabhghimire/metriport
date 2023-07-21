from celery import shared_task

from django.contrib.auth import get_user_model
from api.serializers import HealthMeasurementSerializer
from api.models import HealthMeasurement

from faker import Faker
import requests

User = get_user_model()

fake = Faker()

@shared_task(bind=True)
def get_recent_data(self):
    '''
        A function that runs everyhour.
        Initially developed to send fake request to the same running server to get mock data.
        Due to some error ifself generates fake data for every user, validates it and stores in database.
    '''
    # url = 'django:8000/api/create_mock_data/'
    users = User.objects.all()
    if not users:
        '''creating a superuser if no users are available'''
        us = User.objects.create_user(username='populateuser', password='testpassword', is_superuser=True, is_staff=True, email='test@gmail.com')
        us.save()
        users = User.objects.all()

    for user in users:
        # url = url + str(user.id) + '/'
        # print(url)
        # response = requests.get(url)

        measurements = generate_fake_user_data(user.id)

        # st_code = response.status_code

        # if st_code == 200:

            # measurements = response.json()
        for val in measurements:
            val['user_id'] = user.id 
            serializer = HealthMeasurementSerializer(data=val)
            if serializer.is_valid():
                HealthMeasurement.objects.create(user=user, **serializer.data)
            else:
                return "Data validation Error"
        
        # else:
        #     return f"Something wrong error code."

    return "Got recent Data"

@shared_task(bind=True)
def generate_fake_user_data(self, user_id):
    '''
        Function to generate fake data.
    '''
    measurements = []
    for _ in range(10):
        measurement = {
            'type': fake.random_element(['HeartRate', 'StepCount', 'SleepAnalysis', 'BloodGlucose']),
            'unit': fake.random_element(['count/min', 'count', 'minute', 'mg/dL']),
            'value': fake.random_int(min=50, max=150),
            'startDate': fake.iso8601(tzinfo=None),
            'endDate': fake.iso8601(tzinfo=None),
            'metadata': {'device': fake.random_element(['Apple Watch', 'iPhone', 'Glucose Monitor'])}
        }
        measurements.append(measurement)
    return measurements



