from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.admin import User
from .models import Post,Category,People,Images,Comment
from django.urls import reverse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer,CategorySerializer
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import status




# render Views
@login_required(login_url='/members/login_me_in')
def index(request):
    user_id = request.user.id
    posts =  Post.objects.select_related().prefetch_related('images_set').annotate(comments_Count = Count('comments_post',distinct=True)).annotate(Count('Likes',distinct=True)).all()
    # posts =  Post.objects.select_related().prefetch_related('images_set').all()
    
    print('-'*80)
    array = []
    for post in posts:
        if(post.Likes.filter(id=user_id).exists()):
            isLiked = True
        else:
            isLiked = False
        d={}
        d = {
            'post_id':post.id,
            'user_id':post.user_id,
            'title' : post.title,
            'description':post.description,
            'Tags':post.Tags,
            'category':post.category,
            'userName':post.user.username,
            'images' : post.images_set.all(),
            # 'comments' : post.comments_post.select_related().prefetch_related().all(),
            # 'comments_count': post.comments_post__count,
            'comments_count':post.comments_Count,
            'likesCount' : post.Likes__count,
            # 'actualLikeCount':post.likesCount(),
            # 'actualCommentCount':post.comments_post.count(),
            # 'almost':post.Likes.count(),
            'isLiked':isLiked,
        }
        array.append(d)
    print(array)
    # print(len(array))
    return render(request, template_name='index.html',context={'post':array})

def demo(request):
    return render(request, template_name='Demo.html')

@login_required(login_url='/members/login_me_in')
def demo2(request):
    return render(request, template_name='Demo2.html')

@login_required(login_url='/members/login_me_in')
def Create_a_Post(request):
    return render(request, template_name='Create_a_Post.html')

@login_required(login_url='/members/login_me_in')
def Save_Post_TO_DB(request):
    if(request.method == 'POST'):
        user_id = request.user.id
        title = request.POST.get('Ad-title')
        description = request.POST.get('Ad-Desc')
        Tags = request.POST.get('Ad-Tags')
        category = request.POST.get('category')
        category_d = Category.objects.get(id=category)
        Ad = Post(user_id=user_id,title=title,description=description,Tags=Tags,category=category_d)
        Ad.save()
        Images_list = request.FILES.getlist('file')
        for Image in Images_list:
            Img = Images(Post=Ad,image=Image)
            Img.save()
        return redirect('/')
    return render(request, template_name='index.html')


@login_required(login_url='/members/login_me_in')
def SpecificUser(request,pk):
    user_id = pk
    # user = User.objects.select_related().get(id=user_id)
    person = People.objects.select_related().get(user_id=user_id)
    user_Ads = Post.objects.filter(user_id=user_id)
    favourites = Post.objects.filter(favourites=user_id)
    first_char = person.user.username[0].capitalize()
    # print(first_char)
    context={
        # 'user':user,
        'person':person,
        'user_Ads':user_Ads,
        'favourites':favourites,
        'first_char':first_char
    }
    # print(context)
    # data['person'] = person
    # data['user_Ads'] = user_Ads
    return render(request, template_name='Specific_User_Page.html',context={'Data':context})

def view_post(request,pk):
    # try: 
    post_id = pk
    post = Post.objects.select_related().prefetch_related('images_set','comments_post','comments_post__user').get(id=post_id)
    # images = Images.objects.filter(Post=post)
    # comments = Comment.objects.filter(post=post)
    people = People.objects.select_related().get(user_id=post.user_id)
    context = {
        'post_id':post.id,
        'post_title':post.title,
        'post_description':post.description,
        'post_Tags':post.Tags,
        'post_category':post.category,
        'post_UserId':post.user_id,
        'post_userName':post.user.username,
        'post_images':post.images_set.all(),
        'post_comments':post.comments_post.all(),
        'total_comments':post.comments_post.count(),
        'post_likesCount':post.likesCount(),
        'people':people,
        'first_char':people.user.username[0].capitalize()
    }
    print(context)
    return render(request, template_name='View_Post.html',context={'post_details':context})
    # except:
    #     print('error')
    #     return render(request, template_name='index.html')

@login_required(login_url='/members/login_me_in')
def favourite_post(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if(post.favourites.filter(id=request.user.id).exists()):
            post.favourites.remove(request.user)
        else:
            post.favourites.add(request.user)
    else:
        return redirect('members/login_me_in')
    return redirect(request.META['HTTP_REFERER'])
    # return HttpResponseRedirect(reverse('view_post', args=(post.id,)))

@login_required(login_url='/members/login_me_in')
def comment_post(request,pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        comment = request.POST.get('comment')
        if(comment != ''):
            # print('This is the comment -> ',comment)
            Comment.objects.create(post=post,user=user,comment=comment)
        return redirect(request.META['HTTP_REFERER'])
    return render(request, template_name='index.html')


# API's
# API to Get all the Posts
@api_view()
def View_ALL_Post(request):
    Ads = Post.objects.all()
    serializer = PostSerializer(Ads, many=True)
    return Response(serializer.data)

# API to get all the categories
@api_view()
def Get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

# API to capture comments
@api_view()
def Capture_Comment(request):
    if(request.method == 'POST'):
        user_id = request.user.id
        post_id = request.POST.get('post_id')
        comment = request.POST.get('comment')
        comment_obj = Comment(user_id=user_id,post_id=post_id,comment=comment)
        comment_obj.save()
        return Response('Comment Captured')
    return Response('Something Went Wrong. Error !! ')



@api_view(['GET','POST'])
def like_post(request):
    try:
        if(request.method == 'POST'):
            post_id = request.POST.get('post_id')
            user_id = request.user.id
            post = Post.objects.get(id=post_id)
            if(post.Likes.filter(id=user_id).exists()):
                post.Likes.remove(user_id)
                likesCount = post.Likes.count()
                return JsonResponse({"message":'Like Removed',"status":status.HTTP_200_OK,'id':post_id,'likesCount':likesCount})
            else:
                post.Likes.add(user_id)
                likesCount = post.Likes.count()
                return JsonResponse({"message":"Liked","status": status.HTTP_200_OK,'id':post_id,'likesCount':likesCount})
        return JsonResponse({"message":"Not Allowed"})
    except:
        return JsonResponse({"message":"Something Went Wrong"})

