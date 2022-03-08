from django.urls import path
from . import views


urlpatterns = [
    path('login_me_in/', views.login_user, name='login-in'),
    path('logout_me_out/', views.logout_user, name='logout-out'),
    path('register_user/', views.register_user, name='register-user'),
    
]