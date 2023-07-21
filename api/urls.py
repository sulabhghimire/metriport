from api.views import GetDataView, AccessData

from django.urls import path

urlpatterns = [
    path('create_mock_data/<int:user_id>/', GetDataView.as_view(), name='faker'),
    path('get_data/', AccessData.as_view(), name='data'),
]