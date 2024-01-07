from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from feedback.views import is_valid_indian_number
import random
from datetime import datetime
from .models import Complaint
import os
from twilio.rest import Client

_DEV_ENV = eval(os.getenv('DEV_ENV'))

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        print(message)
        # define the chatbot responses using a dictionary
        chatbot_responses = {
            'Report A Complain': 'Please fill out the complaint form below.',
            'Safety Tips': """1. Use strong and unique passwords: Avoid common words and use a mix of characters. \n
            2. Enable two-factor authentication: Adds an extra layer of security to your accounts.\n
            3. Keep software and systems updated: Ensures that security vulnerabilities are patched.\n
            4. Use a VPN when on public Wi-Fi: Encrypts your internet connection and protects your data.\n
            5. Be cautious of suspicious links and emails: Verify the source before clicking or sharing.\n
            """,
            'End Chat': 'Have a Good Day!',
        }
      
        # look up the response based on the user's message
        response = chatbot_responses[message]
        return JsonResponse({'response': response})
    else:
        return render(request, 'chatbot.html')

@csrf_exempt
def receive_complaint(request):
    if request.method == 'POST':
        # Assuming that the complaint data is sent through POST request
        # Retrieve the data from the request object
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        complaint = request.POST.get('complaint')
        if is_valid_indian_number(phone):
            # Generate 6-digit random ticket ID
            temp_ticket_id = str(random.randint(100000, 999999))
            # Get today's date
            today = datetime.now()
            today_str = today.strftime('%Y%m%d')
            ticket_id = temp_ticket_id[-6:] + today_str[-2:]
            # Register Complain In DB
            register_complaint(name,phone,complaint,ticket_id)
            # Return a success response
            response_data = {'status': 'success', 'ticket_id_main': f'{ticket_id}'}
            return JsonResponse(response_data, status=200)
        else:
            response_data = {'status': 'error', 'message': 'Invalid Phone Number'}
            return JsonResponse(response_data, status=410)

    # Return an error response for all other HTTP methods
    response_data = {'status': 'error', 'message': 'Invalid request method'}
    return JsonResponse(response_data, status=405)

def register_complaint(name, phone, complaint, ticket_id):
    complaint = Complaint(name=name, 
    phone=phone, 
    complaint=complaint, 
    ticket_id=ticket_id,
    ticket_status = False
    )
    # Creating Complain Controller
    account_sid = os.getenv('account_sid')
    auth_token = os.getenv('auth_token')
    client = Client(account_sid, auth_token) 

    # if its in production then only send sms
    if _DEV_ENV == 'False':
        # Senging OTP
        message = client.messages.create(  
                                messaging_service_sid=os.getenv('messaging_service_sid'), 
                                body=f'Your Complaint Ticket Id is: {ticket_id} \n' + 
                                '\nPlease Note this Ticket Id For Reference to Your Complaint!',      
                                to=f'+91{phone}' 
                            )
        complaint.save()
    # just save the responses
    else:
        print(ticket_id)
        complaint.save()