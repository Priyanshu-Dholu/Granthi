from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.shortcuts import render, redirect
from feedback.models import *
from officer.models import User
from .functions import *
from translate import Translator
from chatbot.models import Complaint
import re

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
def updatepassword(request):
    data = {'current': 'updatepassword', 'district': True}
    signed_in_email = request.user
    user = User.objects.get(email=signed_in_email)
    if request.method == 'POST':
        new_password = request.POST.get('new-password')
        current_password = request.POST.get('current-Password')
        confirm_password= request.POST.get('confirm-password')
        
        # Check New Passowrd and Confirm Password
        if new_password == confirm_password:
            if check_password(current_password, user.password):
                if is_secure_password(new_password):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user) 
                    messages.success(request, 'Your password is successfully updated!')
                    return redirect('updatepassword')
                else:
                    messages.error(request, 'Your Password is Not Strong!')
                    return redirect('updatepassword')
            else:
                messages.error(request, 'Current Password is Incorrect!')
                return redirect('updatepassword')
        else:
            messages.error(request, 'New Password and Confirm Password Does Not Match')
            return redirect('updatepassword')

    return render(request,'updatepassword.html',data)

@login_required
def complaints(request):
    complaints = Complaint.objects.order_by('complaint_date')
    total_solved_complaints = Complaint.objects.filter(ticket_status=True).count()
    total_pending_complaints = Complaint.objects.filter(ticket_status=False).count()
    context = {
        'complaints': complaints,
        'total_solved_complaints': total_solved_complaints,
        'total_pending_complaints': total_pending_complaints,
        'current' : complaints,
        'district' : True
    }
    return render(request, 'complaints.html', context)

def update_status(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    complaint.ticket_status = True
    complaint.save()
    return redirect('complaints')

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

        if filter == 'all':
            ps = policestation_view(request)
            if ps == None:
                for que in data:
                    d = Feedback.answer_count(que=que, date=request.GET.get('filter-date'))
                    data[que]['count'] = d
                    data[que]['percentage'] = percentage(d) 
        elif filter == 'ps':
            ps = policestation_view(request)
            if ps != None:
                id=ps
            else:
                id=request.GET.get('id')
            for que in data:
                d = PoliceStation.answer_count(id=id, que=que, sdate=sdate, edate=edate)
                data[que]['count'] = d
                data[que]['percentage'] = percentage(d) 
        elif filter == 'tk':
            ps = policestation_view(request)
            if ps == None:
                for que in data:
                    d = Taluka.answer_count(id=request.GET.get('id'),que=que, sdate=sdate, edate=edate)
                    data[que]['count'] = d
                    data[que]['percentage'] = percentage(d)
        elif filter == 'dt':
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

        if filter == "all":
            data = District.all_names()
        elif filter == "total":
            data = District.total_responses_count(request.GET.get('filter-date'))
        elif filter == "report":
            data = PoliceStation.get_report(id=request.GET.get('id'),sdate=request.GET.get('start-date'), edate=request.GET.get('end-date'))

        return JsonResponse(data)


@login_required
def get_taluka_data(request, filter):
    if request.method == "GET":
        data = {'error': True}

        if filter == "all":
            data = Taluka.all_names(request.GET.get('district-id'))
        elif filter == "report":
            data = PoliceStation.get_report(id=request.GET.get('id'),sdate=request.GET.get('start-date'), edate=request.GET.get('end-date'))

        return JsonResponse(data)

@login_required
def get_police_station_data(request, filter):
    if request.method == "GET":
        data = {'error': True}

        if filter == "all":
            data = PoliceStation.all_names(request.GET.get('taluka-id'))
        elif filter == "report":
            data = PoliceStation.get_report(id=request.GET.get('id'), sdate=request.GET.get('start-date'), edate=request.GET.get('end-date'))

        return JsonResponse(data)



def is_secure_password(password):
    # Check if password has at least 8 characters
    if len(password) < 8:
        return False

    # Check if password has at least 1 uppercase letter
    if not re.search(r'[A-Z]', password):
        return False

    # Check if password has at least 1 digit
    if not re.search(r'\d', password):
        return False

    # Check if password has at least 1 special character
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    # If all checks pass, return True
    return True
