from django.urls import path
from . import views


urlpatterns = [
    # path('', views.index, name='index'),
    path('demo', views.demo, name='demo'),
    # path('demo2', views.demo2, name='demo2'),
    path('',views.demo2,name='demo2'),
    path('add',views.Create_a_Post,name='Add_Post'),
    path('save-Ad' , views.Save_Post_TO_DB , name='Save_Post_TO_DB'),
    path('Profile/<int:pk>/' , views.SpecificUser , name='SpecificUser'),
    path('view-post/<int:pk>/' , views.view_post , name='view_post'),
    path('favourite-post/<int:pk>/',views.favourite_post,name='favourite_post'),
    path('comment-post/<int:pk>/',views.comment_post,name='comment_post'),
    path('search/',views.search,name='search'),
    path('Liked/<int:pk>/',views.Liked_posts,name='Liked_posts'),
    path('Saved/<int:pk>/',views.saved_posts,name='saved_posts'),
    path('Followers/<int:pk>/',views.followers,name='followers'),
    path('Following/<int:pk>/',views.following,name='following'),
    path('getFreePhotos/',views.getFreePhotos,name='Free_photograph'),
    path('getFreePhotograph/',views.getFreePhotograph,name='Free_photograph_form'),
    path('unlock-free-photos/',views.unlock_free_photos_post_ad,name='unlock_free_photos_post_ad'),
    path('order-details/',views.order_details,name='photography_order_details'),
    path('order-confirmed/',views.order_confirmed,name='photography_order_confirmed'),
    path('no-new-photos/',views.come_back_later,name='come_back_later'),
    path('new-post-or-not/',views.Another_Post_or_Not,name='Another_Post_or_Not'),
    
    


    # API URLS
    path('api/view_All_Ads/',views.View_ALL_Post,name='API-View'),
    path('api/get_categories/',views.Get_categories,name='API-Categories'),
    path('api/like_post/',views.like_post,name='API-Like'),
    path('api/HidePost/',views.HidePost,name = 'API-HidePost'),
    path('api/get_post_availablity',views.get_post_availablity,name='API-Product-available-at'),
    path('api/savePost',views.favouritePost,name='API-SavePost'),
    path('api/follow-user/',views.follow_user,name="API-FollowUser"),
    path('api/get_comments/',views.get_comments,name="API-GetComments"),

]