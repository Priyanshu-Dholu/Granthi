from random import randrange
from django.db import models
from django.db.models import Count
from dashboard.functions import *

 

class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=20, null=False)

    # return all district names with id
    @classmethod
    def all_names(cls) -> dict:
        result = cls.objects.values()
        return {r['id']:r['name'] for r in result}
    
    # return total responses count district wise with id
    @classmethod
    def total_responses_count(cls, date) -> dict:
        result = Feedback.objects.filter(date__gte=get_date(date)).values_list('psId__taluka__district').annotate(count=Count('psId__taluka__district'))
        return {i:j for i,j in result}

    # return answer count for particular question of district.
    @classmethod
    def answer_count(cls, district_id:int, que:str, date) -> dict:
        result = Feedback.objects.filter(psId__taluka__district=district_id).filter(date__gte=get_date(date)).values_list(que).annotate(count=Count(que))
        return {i:j for i,j in result}



class Taluka(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=50, null=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='taluka')

    # return all taluka names with id
    @classmethod
    def all_names(cls, district_id) -> dict:
        result = cls.objects.filter(district=district_id).values()
        return {r['id']:r['name'] for r in result}

    # return answer count for particular question of taluka.
    @classmethod
    def answer_count(cls, taluka_id:int, que:str, date) -> dict:
        result = Feedback.objects.filter(psId__taluka=taluka_id).filter(date__gte=get_date(date)).values_list(que).annotate(count=Count(que))
        return {i:j for i,j in result}


class PoliceStation(models.Model):
    id = models.AutoField(primary_key=True)
    qrId = models.IntegerField(null=False, unique=True, db_index=True, default=randrange(000000,999999))
    name = models.TextField(max_length=200, null=False)
    taluka = models.ForeignKey(Taluka, on_delete=models.CASCADE, related_name='policestation')
    isSubDiv = models.BooleanField(default=False)

    # return all Police Station names with id
    @classmethod
    def all_names(cls, taluka_id) -> dict:
        result = cls.objects.filter(taluka=taluka_id).values()
        return {r['id']:r['name'] for r in result}

    # return answer count for particular question of Police Station.
    @classmethod
    def answer_count(cls, id:int, que:str, date) -> dict:
        result = Feedback.objects.filter(psId=id).filter(date__gte=get_date(date)).values_list(que).annotate(count=Count(que))
        return {i:j for i,j in result}


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

    # Return Total feedbacks
    @classmethod
    def total(cls):
        return cls.objects.count()

    # count feedback answer for particular question ~ 'column name'
    # Ex: groupby_count('q1')
    # Dashboard overview questions report 
    @classmethod
    def answer_count(cls, que:str, date) -> dict:
        result = cls.objects.filter(date__gte=get_date(date)).values_list(que).annotate(count=Count(que))
        return {i:j for i,j in result} 

