from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def debug(data, message=''):
    print(f"::  [ {data} ] ----- {message} -----")


def Login(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        debug(user) 
        if user is not None:
            login(request, user=user)
            debug(user.email, 'login done!')            
            return redirect('dashboard')
        else:
            debug('can\'t login')
            messages.error(request, 'Invalid email or password. Please try again.')
            return render(request, 'admin-login.html')
    else:
        return render(request, 'admin-login.html')

@login_required
def Logout(request):
    logout(request)
    return redirect('login')