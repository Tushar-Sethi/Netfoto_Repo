from django.urls import path
from . import views


urlpatterns = [
    path('login_me_in/', views.login_user, name='login-in'),
    path('logout_me_out/', views.logout_user, name='logout-out'),
    path('register_user/', views.register_user, name='register-user'),
    # path('verify-email/',views.verify_email,name='verify-email-username'),
    path('verify-email/<str:username>/ ', views.verify_email, name='verify-email'), 
    path('resend-email/', views.resend_email, name='resend-email'),
    path('profile/', views.User_Profile, name='User_Profile'),
]