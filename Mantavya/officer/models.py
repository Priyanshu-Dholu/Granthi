from django.contrib.auth.models import AbstractUser
from django.db import models
from feedback.models import District, Taluka, PoliceStation
from django.utils.translation import gettext_lazy as _


from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    view = models.IntegerField()
    '''
    district - 3
    taluka - 2
    police station - 1
    '''
    view_id = models.IntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email   

    def get_view(self):
        data = 0
        match self.view:
            case 3:
                data = District.objects.get(id=self.view_id)
            case 2:
                data = Taluka.objects.get(id=self.view_id)
            case 1:
                data = PoliceStation.objects.get(id=self.view_id)
        return data
