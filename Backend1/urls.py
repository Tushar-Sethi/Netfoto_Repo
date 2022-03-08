from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('demo', views.demo, name='demo'),
    path('demo2', views.demo2, name='demo2'),
    path('add',views.Create_a_Post,name='Add_Post'),
    path('save-Ad' , views.Save_Post_TO_DB , name='Save_Post_TO_DB'),
    path('Profile/<int:pk>/' , views.SpecificUser , name='SpecificUser'),
    path('view-post/<int:pk>/' , views.view_post , name='view_post'),
    path('favourite-post/<int:pk>/',views.favourite_post,name='favourite_post'),
    path('comment-post/<int:pk>/',views.comment_post,name='comment_post'),
    


    # API URLS
    path('api/view_All_Ads/',views.View_ALL_Post,name='API-View'),
    path('api/get_categories/',views.Get_categories,name='API-Categories'),
    path('api/like_post/',views.like_post,name='API-Like'),

]