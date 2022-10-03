from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="dashboard"),
    path('detailed', views.detailed, name="Detailed"),
    path('get/question/<str:filter>', views.get_question_data),
    path('get/district/<str:filter>', views.get_district_data),
    path('get/taluka/<str:filter>', views.get_taluka_data),
    path('get/policestation/<str:filter>', views.get_police_station_data),
]
