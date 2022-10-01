from django.http import JsonResponse
from django.shortcuts import render
from feedback.models import *
import datetime as dt

QUESTIONS = ['q1', 'q2', 'q3'] 

# Create your views here.
def index(request):
    return render(request, 'index.html')

def percentage(data:dict) -> dict:
    s = sum(data.values())
    return { n:(data[n]/s)*100 for n in data }


'''
today
last 7 days
last 30 days
last 90 days
last 365 days
All time
'''
def get_date(l:str):
    today = dt.datetime.now()
    
    if l == "td":
        return today.date()
    elif l == "l7d":
        d = today - dt.timedelta(days=7)
    elif l == "l30d":
        d = today - dt.timedelta(days=30)
    elif l == "l90d":
        d = today - dt.timedelta(days=90)
    elif l == "l356d":
        d = today - dt.timedelta(days=365)
    
    return d.date() 


def get_question_data(request, filter:str):
    '''
    filter-date: datetime
    filter-table: ['all', 'ps', 'tk', 'dt']
    '''
    if request.method == "POST":
            
        data = {'q1': {},'q1': {},'q3': {}}

        if filter == "all":
            for que in data:
                d = groupby_question_count(que)
                data[que]['count'] = d
                data[que]['percentage'] = percentage(d)
        # elif filter == "ps":    

        return data

# count feedback answer for particular question ~ 'column name'
# Ex: groupby_count('q1')
# Dashboard overview questions report 
def groupby_question_count(que:str, l):
    if que in QUESTIONS:
        result = Feedback.objects.filter(date__gte=get_date(l)).values_list(que).annotate(count=Count(que))
        return {i:j for i,j in result} 
    return

# def count_answer(filter:str, id:int, que:str):


def policestation_answer_count(id:int, que:str):
    if que in QUESTIONS:
        result = Feedback.objects.filter(psId=id).values_list(que).annotate(count=Count(que))
        return {i:j for i,j in result}

    return

# return answer count for particular question of taluka.
def taluka_answer_count(id:int, que:str):
    if que in QUESTIONS:
        result = Feedback.objects.filter(psId__taluka=id).values_list(que).annotate(count=Count(que))
        return {i:j for i,j in result}

    return

# return answer count for particular question of district.
def district_answer_count(id:int, que:str):
    if que in QUESTIONS:
        result = Feedback.objects.filter(psId__taluka__district=id).values_list(que).annotate(count=Count(que))
        return {i:j for i,j in result}

    return

def groupby_district_total_count():
    result = Feedback.objects.values_list('psId__taluka__district').annotate(count=Count('psId__taluka__district'))
    return {i:j for i,j in result}


def total_feedbacks():
    return Feedback.objects.count()


