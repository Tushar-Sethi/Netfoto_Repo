from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.models import User
from Backend1.models import People

def login_user(request):
    if request.method == 'POST':
        print('-'*100)
        username = request.POST['username']
        password = request.POST['password']
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
        if(request.user.is_authenticated):
            return redirect('index')
        return render(request, 'registration/Login.html')

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
                    messages.success(request, ("You are now registered and can log in"))
                    return redirect('login-in')
        else:
            messages.success(request, ("Passwords do not match"))
            return redirect('register-user')
    return render(request, 'registration/Register.html')