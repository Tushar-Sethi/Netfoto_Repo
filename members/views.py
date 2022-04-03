from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from Backend1.models import People,product_orders
import math
import random
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from random_username.generate import generate_username
import random
import string
import re
from datetime import datetime,timezone


from django.contrib.auth.hashers import make_password


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if(User.objects.filter(username=username).exists()):
            user = User.objects.filter(username=username)
        elif(User.objects.filter(email=username).exists()):
            user = User.objects.filter(email=username)
            username = user[0].username
        else:
            messages.success(request, ("Username or Email Does Not Exist"))
            return redirect('register-user')
        Is_verified = user[0].people.is_verified
        if (Is_verified == True):
            print(username)
            print(password)
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

def Random_Password(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def logout_user(request):
    logout(request)
    # messages.success(request, ("You are now logged out"))
    return redirect('first')


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
                    people = People.objects.create(user_id=user.id,email=email)
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
                user.first_name = request.POST['First_Name']
                user.last_name = request.POST['Last_Name']
                people = People.objects.get(user__username=user.username)
                people.Phone_number = request.POST['Phone_Number']
                people.Birth_Date = request.POST['Birth_Date']
                # people.photo = request.files['Profile_Photo']
                profile_photo = request.FILES.get('profile_photo')
                print(profile_photo)
                if(profile_photo != None):
                    people.photo = request.FILES['profile_photo']
                user.save()
                people.save()
                messages.success(request, ("Profile Updated"))
                return redirect('User_Profile')
        else:
            user = request.user
            profile = People.objects.get(user__username=user.username)
            profile_array={
                'First_Name': user.first_name,
                'Last_Name': user.last_name,
                'phone_number': profile.Phone_number,
                'Birth_Date': profile.Birth_Date,
                'photo': profile.photo
            }
            return render(request, 'registration/Profile.html', context = {'profile': profile_array})
            
    else:
        return redirect('login-in')


def first(request):
    return render(request, 'registration/First_Page.html')


def checkValidEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True

    else:
        return False


def CheckEmail(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        if(User.objects.filter(email=email).exists()):
            return JsonResponse({'message': 'Login', 'status': 'success'})
        else:
            if(checkValidEmail(email)):
                OTP = generateOTP()
                send_verification_email(OTP, email)
                username = generate_username()
                # password = Random_Password(8)
                password = '123'
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                people = People.objects.create(user_id=user.id, OTP=OTP)
                people.save()
                return JsonResponse({'message': 'Register'})
            else:
                return JsonResponse({'message': 'Invalid Email', 'status': 'error'})
    else:
        return redirect('login-in')
        
def check_OTP(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        OTP = request.POST['OTP']
        people = People.objects.get(user__email=email)
        if(people.OTP == OTP):
            people.is_verified = True
            people.save()
            print('verified')
            return JsonResponse({'message': 'Verified', 'status': 'success'})
        else:
            return JsonResponse({'message': 'Invalid OTP', 'status': 'error'})
    else:
        return redirect('login-in')

def login_register(request):
    if(request.method == 'POST'):
        if 'login' in request.POST:
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.get(email=email)
            username = user.username
            Is_verified = user.people.is_verified
            if (Is_verified == True):
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    people = People.objects.get(user__username=username)
                    if(product_orders.objects.filter(people_id=people.id).exists()):
                        PO = product_orders.objects.filter(people_id=people.id).all().order_by('-id')[0]
                        if((datetime.now(timezone.utc) - PO.created_date).days > 30):
                            people.step_1 = False
                            people.step_2 = False
                            people.step_3 = False
                            people.save()
                    if request.GET.get('next', None):
                        return redirect(request.GET['next'])
                    return redirect('demo2')
                else:
                    messages.success(request, ("Invalid credentials"))
                    return redirect('first')
            else:
                messages.success(request, ("You need to verify your email first"))
                return redirect('verify-email', username=username)
        elif 'register' in request.POST:
            email = request.POST['email']
            password1 = request.POST['register-Password']
            password2 = request.POST['register-confirm-password']
            name = request.POST['Name']
            username = request.POST['username']
            if(password1 == password2):
                user = User.objects.filter(email=email)
                user.update(username=username)
                user1 = User.objects.get(username=username)
                user1.set_password(password1)
                user1.save()
                people = People.objects.get(user__email=email)
                people.Name = name
                people.save()
                if(people.is_verified == True):
                    user = authenticate(request, username=username, password=password1)
                    if user is not None:
                        login(request, user)
                        return redirect('demo2')
                    else:
                        messages.success(request, ("Invalid credentials"))
                        # return redirect('first')
                else:
                    messages.success(request, ("You need to verify your email first"))
                    # return redirect('verify-email', username=username)
            else:
                messages.success(request, ("Passwords do not match"))
                return redirect('first')
    return redirect('first')

    
def check_username(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        print(username)
        if(User.objects.filter(username=username).exists()):
            return JsonResponse({'message': 'Not Available', 'status': 'error'})
        else:
            return JsonResponse({'message': 'Available', 'status': 'success'})
    else:
        print('error')


def reset_password(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        user = User.objects.get(email=email)
        username = user.username
        #reset link

        send_reset_email(username, password, email)
        return JsonResponse({'message': 'Password Reset'})
    return render(request, template_name='registration/reset-password.html')