from django.urls import path
from .views import chatbot_view, receive_complaint

urlpatterns = [
    path('', chatbot_view, name='chatbot'),
    path('complaint/', receive_complaint, name='complaint')
]
