from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404, JsonResponse
import os
from twilio.rest import Client
from random import randint
import datetime 
from translate import Translator
from .models import Citizen, Feedback, AnswerList, PoliceStation
import phonenumbers

translator = Translator(from_lang = "en",to_lang="gu-IN")

_SESSION_EXPIRY = int(os.getenv('SESSION_EXPIRY'))   # in seconds
_DEV_ENV = eval(os.getenv('DEV_ENV'))
_USE_TWILIO = eval(os.getenv('USE_TWILIO'))

# class Session:
def otpVerified(request):
    if 'otp-verified' in request.session:
        if request.session['otp-verified']:
            return True
    
    return False

feedback_id = "123456"

# Function to Get Feedback Values
def getFeedback(request):

    # Generate random 4-digit number
    random_number = randint(1000, 9999)

    # Get current day
    current_date = datetime.datetime.now().day

    # Combine random number and current date
    global feedback_id
    feedback_id = str(random_number) + str(current_date).zfill(2)
    mnum = request.session['Mobile-Num']
    if request.method == "POST":
        if otpVerified(request):
            send_message(f'Your Feedback ID is: {feedback_id}', mnum)
            cID = Citizen.objects.get(mobileNum=request.session['Mobile-Num'])
            q1 = request.POST.get('1')
            q2 = request.POST.get('2')
            q3 = request.POST.get('3')
            q4 = request.POST.get('4')

            Feedback(
                citizenId=cID, 
                name = request.session['name'],
                q1 = AnswerList.objects.get(id=q1),
                q2 = AnswerList.objects.get(id=q2),
                q3 = AnswerList.objects.get(id=q3), 
                q4 = q4, 
                psId = PoliceStation.objects.get(qrId=request.session['qrid']),
                feedback_id = feedback_id
                ).save()

            return JsonResponse({'Status': True})

# Function to send message / otps using twilio
def send_message(text, receiver_phone):
    # Send SMS only if Twilio is set and it's in Production Environment
    if _USE_TWILIO == True and _DEV_ENV == False:
        if is_valid_indian_number(receiver_phone):
            print("Sending Message")
            account_sid = os.getenv('account_sid')
            auth_token = os.getenv('auth_token')
            client = Client(account_sid, auth_token)
            message = client.messages.create(  
                messaging_service_sid=os.getenv('messaging_service_sid'), 
                body=text,      
                to=f'+91{receiver_phone}' 
            )  
            print("Message Sent:\n", message)
            return True
        else:
            print("Invalid Phone Number")
            return False
    else:
        print("Message cannot be sent as Twilio is not set or in development mode")
        return True


def generate_OTP(request):
    n = randint(100000, 999999)
    request.session['OTP'] = n  
    mnum = request.session['Mobile-Num']
    if is_valid_indian_number(mnum):
        if _USE_TWILIO == True and _DEV_ENV == False:
            print("Sending OTP")
            send_message(f'Your OTP For Granthi is: {n}', mnum)
            print("OTP Sent Successfully!")
            print(f"{request.session['Mobile-Num']} :OTP: {n}")
            return True
        else:
            print('OTP In Terminal')
            print(f"{request.session['Mobile-Num']} :OTP: {n}")
            return True
    else:
        messages.error(request, 'Invalid Phone Number!')
        return False

    
def resendOTP(request):
    generate_OTP(request)
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
        
        # if number verified return feedback form
        if otpVerified(request):
            data['name'] = request.session['name']
            data['mobile_num'] = request.session['Mobile-Num']
            
            return render(request, 'feedback.html', data)
    
        # else Login Form
        return render(request,'login.html', data)

    if request.method == 'POST':
        # verifying mobile number [login]
        name = request.POST.get('name')
        mobile_num = request.POST.get("mobile-num")

        # save name & mobile number in session
        request.session['name'] = name
        request.session['Mobile-Num'] = mobile_num
        request.session['qrid'] = qrid

        # insert mobile number if not exists in db
        if not Citizen.objects.filter(mobileNum=mobile_num).exists():
            citizen = Citizen(1, int(mobile_num))
            citizen.save()
            print("Record Added")

        # generate otp & save otp in session
        if generate_OTP(request):
            # set session expiry 5 mins
            request.session.set_expiry(_SESSION_EXPIRY)
            return redirect('verify-otp')
        else:
            psname = PoliceStation.objects.get(qrId=qrid).name
            data = {
                'ps': psname,
                "gu_ps" : translator.translate(psname),
                'psid': qrid
            }
            return render(request,'login.html',data)
    raise Http404('Police Station Does not exist.')

# Verifying Phone Number
def is_valid_indian_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, "IN")
        return phonenumbers.is_valid_number(parsed_number) and \
            phonenumbers.is_possible_number(parsed_number) and \
            phonenumbers.phonenumberutil.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE
    except phonenumbers.phonenumberutil.NumberParseException:
        return False

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
                messages.error(request, "Invalid OTP, Please Try Again!")
        
            return render(request, 'verify-otp.html', data)
        
        return redirect('Home')

def thanku(request):
    global feedback_id
    data = {
        'feedback_id': feedback_id
    }
    request.session.flush()
    return render(request, 'thanku.html', data)