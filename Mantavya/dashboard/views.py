from tkinter.tix import Tree
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from feedback.models import *
from officer.models import User
from .functions import *

from translate import Translator

translator = Translator(from_lang = "en",to_lang="gu-IN")

QUESTIONS = ['q1', 'q2', 'q3'] 

#Function
def policestation_view(request):
    cu = request.user
    if cu.view == 1: # Police Station level View
        return cu.get_view()
    return None


@login_required
def index(request):
    data = {'current': 'overview', 'district': True}
    ps = policestation_view(request)
    if ps != None:
        data['district'] = False
        return redirect('Detailed')

    return render(request, 'index.html',  data)

@login_required
def detailed(request):
    data = {'current': 'detailed', 'district': True}
    ps = policestation_view(request)
    if ps != None:
        data['district'] = False        
        data['psid'] = ps.id
        data['ps_name'] = ps.name
    return render(request, 'detailed.html', data)

@login_required
def qrgenerator(request):
    data = {'current': 'qrgenerator', 'district': True}
    ps = policestation_view(request)
    if ps != None:
        data['district'] = False 
        data['psid'] = ps.id
        data['ps_name'] = ps.name  
    return render(request, 'qr-generator.html', data)

@login_required
def get_question_data(request, filter):
    '''
    filter-date: datetime
    filter-table: ['all', 'ps', 'tk', 'dt']
    '''
    if request.method == "GET":
        sdate = request.GET.get('start-date') 
        edate = request.GET.get('end-date')
        print('===++++=====', sdate, edate)
        data = {'q1': {},'q2': {},'q3': {}}

        match filter:
            case 'all':
                ps = policestation_view(request)
                if ps == None:
                    for que in data:
                        d = Feedback.answer_count(que=que, date=request.GET.get('filter-date'))
                        data[que]['count'] = d
                        data[que]['percentage'] = percentage(d)  
            case 'ps':
                ps = policestation_view(request)
                if ps != None:
                    id=ps
                else:
                    id=request.GET.get('id')
                for que in data:
                    d = PoliceStation.answer_count(id=id, que=que, sdate=sdate, edate=edate)
                    data[que]['count'] = d
                    data[que]['percentage'] = percentage(d) 
            case 'tk':
                ps = policestation_view(request)
                if ps == None:
                    for que in data:
                        d = Taluka.answer_count(id=request.GET.get('id'),que=que, sdate=sdate, edate=edate)
                        data[que]['count'] = d
                        data[que]['percentage'] = percentage(d)
            case 'dt':
                ps = policestation_view(request)
                if ps == None:
                    for que in data:
                        d = District.answer_count(id=request.GET.get('id'),que=que, sdate=sdate, edate=edate)
                        data[que]['count'] = d
                        data[que]['percentage'] = percentage(d)
        return JsonResponse(data)

@login_required
def get_qrid(request):
    if request.method == "GET":
        ps = PoliceStation.objects.get(id=request.GET.get('psid'))
        data = {'qrid' : ps.qrId, 'ename': ps.name, 'gname': translator.translate(ps.name)}
        return JsonResponse(data)

@login_required
def get_district_data(request, filter):
    if request.method == "GET":
        data = {'error': True}

        match filter:
            case "all":
                data = District.all_names()
            case "total": 
                data =  District.total_responses_count(request.GET.get('filter-date'))
            case "report":
                data = PoliceStation.get_report(id=request.GET.get('id'),sdate = request.GET.get('start-date'), edate = request.GET.get('end-date'))
        return JsonResponse(data)

@login_required
def get_taluka_data(request, filter):
    if request.method == "GET":
        data = {'error': True}

        match filter:
            case "all":
                data = Taluka.all_names(request.GET.get('district-id'))
            case "report":
                data = PoliceStation.get_report(id=request.GET.get('id'),sdate = request.GET.get('start-date'), edate = request.GET.get('end-date'))
        return JsonResponse(data)

@login_required
def get_police_station_data(request, filter):
    if request.method == "GET":
        data = {'error': True}

        match filter:
            case "all":
                data = PoliceStation.all_names(request.GET.get('taluka-id'))
            case "report":
                data = PoliceStation.get_report(id=request.GET.get('id'),sdate = request.GET.get('start-date'), edate = request.GET.get('end-date'))                
        return JsonResponse(data)
