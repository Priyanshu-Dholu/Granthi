from random import randrange
from django.db import models
from django.db.models import Count


class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=20, null=False)

class Taluka(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50, null=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='taluka')

class PoliceStation(models.Model):
    id = models.AutoField(primary_key=True)
    qrId = models.IntegerField(null=False, unique=True, db_index=True, default=randrange(000000,999999))
    name = models.TextField(max_length=200, null=False)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE, related_name='policestation')
    isSubDiv = models.BooleanField(default=False)

class SubDivPoliceStation(models.Model):
    subDivision = models.ForeignKey(PoliceStation, on_delete=models.CASCADE, related_name="subDivision")
    policeStation = models.ForeignKey(PoliceStation, on_delete=models.CASCADE, related_name="policeStation")

class AnswerList(models.Model):
    id = models.AutoField(primary_key=True)
    answer = models.TextField(max_length=200, default='')
        
class Citizen(models.Model):
    id = models.AutoField(primary_key=True)
    mobileNum = models.CharField(null=False, unique=True, max_length=10, db_index=True)

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    citizenId = models.ForeignKey(Citizen, on_delete=models.CASCADE)
    name = models.TextField(max_length=50)
    q1 = models.ForeignKey(AnswerList, on_delete=models.CASCADE, related_name="q1")
    q2 = models.ForeignKey(AnswerList, on_delete=models.CASCADE, related_name="q2")
    q3 = models.ForeignKey(AnswerList, on_delete=models.CASCADE, related_name="q3")
    q4 = models.TextField(max_length=300)
    psId = models.ForeignKey(PoliceStation, on_delete=models.CASCADE, related_name='feedback')
    date = models.DateField()