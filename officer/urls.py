from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.Login, name="login"),
    path('logout', views.Logout,  name="logout"),
    path('dashboard/', include('dashboard.urls'), name='dashboard'),
]
