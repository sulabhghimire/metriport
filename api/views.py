from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.tasks import generate_fake_user_data

from api.serializers import HealthMeasurementSerializer, AllHealthMeasurementSerializer
from api.models import HealthMeasurement

class AccessData(APIView):

    def get(self, request):
        user_id = request.GET.get('user_id')
        if not user_id:
            values = HealthMeasurement.objects.all()
            serializer = AllHealthMeasurementSerializer(values, many=True)
        else:
            try:
                values = HealthMeasurement.objects.filter(user__id=user_id)
                serializer = AllHealthMeasurementSerializer(values, many=True)
            except:
                return Response({'msg' :'No such user has been found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'msg': 'Data sucessfully fetched.', 'data':serializer.data}, status=status.HTTP_200_OK)

class GetDataView(APIView):

    def get(self, request, user_id):
        
        if not user_id:
            return Response({'msg': 'user_id is required.'}, status=404)

        measurements = generate_fake_user_data(int(user_id))
        serializer = HealthMeasurementSerializer(data=measurements, many=True)

        if serializer.is_valid():
            data_status = status.HTTP_201_CREATED
            data_msg = "Mock data generated"
            data = serializer.validated_data
        else:
            data_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            data_msg = "Some error has occured"
            data = serializer.errors

        return Response({'msg' : data_msg, 'data': data}, status=data_status)