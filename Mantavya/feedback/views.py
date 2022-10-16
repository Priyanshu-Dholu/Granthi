from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, JsonResponse

from random import randrange
from translate import Translator

from .models import Citizen, Feedback, AnswerList, PoliceStation

translator = Translator(from_lang = "en",to_lang="gu-IN")

_SESSION_EXPIRY = 300   # in seconds

def debug(n):
    print('+'*20,n,'+'*20)

# class Session:
def otpVerified(request):
    if 'otp-verified' in request.session:
        if request.session['otp-verified']:
            return True
    
    return False


def getFeedback(request):
    # Get Feedback
    if request.method == "POST":
        debug("Get Feedback Response ")
        if otpVerified(request):
            
            cID = Citizen.objects.get(mobileNum=request.session['Mobile-Num'])
            q1 = request.POST.get('1')
            q2 = request.POST.get('2')
            q3 = request.POST.get('3')
            q4 = request.POST.get('4')

            Feedback(
                citizenId=cID, 
                name = request.session['Name'],
                q1 = AnswerList.objects.get(id=q1),
                q2 = AnswerList.objects.get(id=q2),
                q3 = AnswerList.objects.get(id=q3), 
                q4 = q4, 
                psId = PoliceStation.objects.get(qrId=request.session['qrid'])
                ).save()

            request.session.flush()
            return JsonResponse({'Status': True})

def generateOTP(request):
    n = randrange(000000,999999)
    request.session['OTP'] = n
    debug(f"{request.session['Mobile-Num']} :OTP: {n}")
    
def resendOTP(request):
    generateOTP(request)
    messages.success(request, "A new otp has been sent. :)")
    return redirect('verify-otp')

# verifying mobile number, send OTP, reutrn feedback form
def feedback(request, qrid):
    if request.method == 'GET':
        psname = PoliceStation.objects.get(qrId=qrid).name
        data = {
            'ps': psname,
            "gu_ps" : translator.translate(psname),
            'psid': qrid
        }
        
        # if number verified reutnr feedback form
        if otpVerified(request):
            data['name'] = request.session['Name']
            data['mobile_num'] = request.session['Mobile-Num']
            
            return render(request, 'feedback.html', data)
    
        # else Login Form
        return render(request,'login.html', data)

    if request.method == 'POST':
        # verifying mobile number [login]
        name = request.POST.get('name')
        mobile_num = request.POST.get("mobile-num")

        # save name & mobile number in session
        request.session['Name'] = name
        request.session['Mobile-Num'] = mobile_num
        request.session['qrid'] = qrid

        # insert mobile number if not exists in db
        if not Citizen.objects.filter(mobileNum=mobile_num).exists():
            citizen = Citizen(1, int(mobile_num))
            citizen.save()
            debug("Record added")

        # generate otp & save otp in session
        generateOTP(request)

        # set session expiry 5 mins
        request.session.set_expiry(_SESSION_EXPIRY)
        
        return redirect('verify-otp')

    raise Http404('Police Station Does not exist.')
    
# verifying OTP
def verify_otp(request):
    qrid = request.session['qrid']
    if 'Mobile-Num' not in request.session:
        return redirect('feedback', qrid)

    data = {
        'mobile_num': request.session['Mobile-Num'][-3:],
        're_sec':'60'
    }
    
    if request.method == 'GET':
        return render(request, 'verify-otp.html', data)

    elif request.method == 'POST':
        if 'OTP' in request.session:
            # check if otp is valid
            if int("".join(request.POST.getlist('otp'))) == request.session['OTP']:
                request.session['otp-verified'] = True
                del request.session['OTP']
                return redirect('feedback', qrid)
            else: 
                request.session['otp-verified'] = False
                messages.error(request, "invalid otp. please check your code and try again")
        
            return render(request, 'verify-otp.html', data)
        
        return redirect('Home')

def thanku(request):
    return render(request, 'thanku.html')