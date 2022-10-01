from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="tools"),
    path('insert-district-taluka-data', views.insertData),
    path('insert-test-dataset', views.insertTestDataSet),
    path('insert-Feedback-Dataset',views.insertFeedbackDataSet),
]
