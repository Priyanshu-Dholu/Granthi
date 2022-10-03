from django.urls import path
from . import views

urlpatterns = [
    path('feedback/<int:qrid>', views.feedback, name="feedback"),
    path('feedback/send', views.getFeedback, name='get-feedback'),
    path('verify-otp', views.verify_otp, name='verify-otp'),
    path('verify-otp/resend', views.resendOTP, name='resend-otp'),
    path('feedback/submitted', views.thanku, name="submitted")
]
