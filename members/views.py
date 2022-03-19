from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from Backend1.models import People
import math
import random
from django.conf import settings
from django.core.mail import send_mail


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username)
        Is_verified = user[0].people.is_verified
        if (Is_verified == True):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.GET.get('next', None):
                    return redirect(request.GET['next'])
            # messages.success(request, ("You are now logged in"))
                return redirect('index')
            else:
                messages.success(request, ("Invalid credentials"))
                return redirect('login')
        else:
            messages.success(request, ("You need to verify your email first"))
            return redirect('verify-email', username=username)
    else:
        if(request.user.is_authenticated):
            return redirect('index')
    return render(request, 'registration/Login.html')

def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP


def logout_user(request):
    logout(request)
    messages.success(request, ("You are now logged out"))
    return redirect('login-in')


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        First_Name = request.POST['First_Name']
        Last_Name = request.POST['Last_Name']
        # phone_number = request.POST['phone_number']
        if (password == password2):
            if (User.objects.filter(username=username).exists()):
                messages.success(request, ("Username already Taken"))
                return redirect('register-user')
            else:
                if (User.objects.filter(email=email).exists()):
                    messages.success(request, ("Email already exists"))
                    return redirect('login-in')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=First_Name, last_name=Last_Name)
                    user.save()
                    people = People.objects.create(user_id=user.id)
                    people.save()
                    messages.success(request, ("Please Verify you email by entering the OTP sent to your email"))
                    OTP = generateOTP()
                    people.OTP = OTP
                    people.save()
                    send_verification_email(OTP, email)
                    return redirect('verify-email', username=username)
        else:
            messages.success(request, ("Passwords do not match"))
            return redirect('register-user')
    return render(request, 'registration/Register.html')


def verify_email(request,username=''):
    if request.method == 'POST':
        if(username == '' or username == None or username == 'None' or username == 'none' or username == 'null' or username == 'Null'):
            messages.success(request, ("Please Enter a Correct Username"))
            return redirect('verify-email')
        username = request.POST['username']
        token = request.POST['token']
        is_Verified = User.objects.filter(username=username)[0].people.is_verified
        if(is_Verified == False):
            people_OTP = People.objects.get(user__username=username).OTP
            if (people_OTP == token):
                people = People.objects.get(user__username=username)
                people.is_verified = True
                people.save()
                messages.success(request, ("Email Verified"))
                return redirect('login-in')
            else:
                messages.success(request, ("Invalid OTP"))
                return redirect('verify-email', token=token)
        else:
            messages.success(request, ("Email already verified"))
            return redirect('login-in')
    return render(request, 'registration/Verify.html', {'username': username})


def send_verification_email(OTP, email):
    subject = 'Verify your email'
    message = 'your OTP is ' + OTP
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )
    return True


def resend_email(request):
    if(request.method == 'POST'):
        try:
            username = request.POST['username']
            user = User.objects.filter(username=username)
            email = user[0].email
            OTP = generateOTP()
            people = People.objects.get(user__username=username)
            people.OTP = OTP
            people.save()
            send_verification_email(OTP, email)
            messages.success(request, ("Email Sent"))
            return redirect('verify-email', username=username)
        except:
            messages.success(request, ("Please Enter a Correct Username"))
            return redirect('verify-email') 
    return render(request, 'registration/Resend.html')    

def User_Profile(request):
    if(request.user.is_authenticated):
        if request.method == 'POST':
                user = request.user
                people = People.objects.get(user__username=user.username)
                people.First_Name = request.POST['First_Name']
                people.Last_Name = request.POST['Last_Name']
                people.phone_number = request.POST['phone_number']
                people.Birth_Date = request.POST['Birth_Date']
                people.photo = request.FILES['photo']
                people.save()
                messages.success(request, ("Profile Updated"))
                return redirect('User_Profile')
        else:
            user = request.user
            profile = People.objects.get(user__username=user.username)
            return render(request, 'registration/Profile.html', {'profile': profile})
            
    else:
        return redirect('login-in')
        
