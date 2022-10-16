from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="tools"),
    path('insert-district-taluka-data', views.insertData),
    path('insert-test-dataset', views.insertTestDataSet),
    path('insert-Feedback-Dataset',views.insertFeedbackDataSet),
    path('insert_users_data', views.insert_users_data),
    path('insert_police_station_user_data', views.insert_police_station_user_data),
]
