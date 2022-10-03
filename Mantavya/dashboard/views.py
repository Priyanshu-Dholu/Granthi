from django.http import JsonResponse
from django.shortcuts import render
from feedback.models import *
from .functions import *

QUESTIONS = ['q1', 'q2', 'q3'] 


def index(request):
    return render(request, 'index.html')

def detailed(request):
    return render(request, 'detailed.html')


def get_question_data(request, filter):
    '''
    filter-date: datetime
    filter-table: ['all', 'ps', 'tk', 'dt']
    '''
    if request.method == "GET":
        date = request.GET.get('filter-date') 

        data = {'q1': {},'q2': {},'q3': {}}

        match filter:
            case 'all':
                for que in data:
                    d = Feedback.answer_count(que, date)
                    data[que]['count'] = d
                    data[que]['percentage'] = percentage(d)  
            case 'ps':
                for que in data:
                    d = PoliceStation.answer_count(id=request.GET.get('id'),que=que, date=date)
                    data[que]['count'] = d
                    data[que]['percentage'] = percentage(d)  
            case 'tk':
                for que in data:
                    d = Taluka.answer_count(id=request.GET.get('id'),que=que, date=date)
                    data[que]['count'] = d
                    data[que]['percentage'] = percentage(d)
            case 'dt':
                for que in data:
                    d = District.answer_count(id=request.GET.get('id'),que=que, date=date)
                    data[que]['count'] = d
                    data[que]['percentage'] = percentage(d)
        return JsonResponse(data)

def get_district_data(request, filter):
    if request.method == "GET":
        data = {'error': True}

        match filter:
            case "all":
                data = District.all_names()
            case "total": 
                data =  District.total_responses_count(request.GET.get('filter-date'))
        
        return JsonResponse(data)

def get_taluka_data(request, filter):
    if request.method == "GET":
        data = {'error': True}

        match filter:
            case "all":
                data = Taluka.all_names(request.GET.get('district-id'))

        return JsonResponse(data)

def get_police_station_data(request, filter):
    if request.method == "GET":
        data = {'error': True}

        match filter:
            case "all":
                data = PoliceStation.all_names(request.GET.get('taluka-id'))
                
        return JsonResponse(data)



# def count_answer(filter:str, id:int, que:str):




