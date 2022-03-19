from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.admin import User
from .models import Post,Category,People,Images,Comment,ProductAvailability
from django.urls import reverse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer,CategorySerializer,ProductAvailabilitySerializer
from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import status
from datetime import datetime,timezone
# render Views
@login_required(login_url='/members/login_me_in')
def index(request):
    user_id = request.user.id
    posts =  Post.objects.exclude(users=request.user)\
    .select_related('user__people','ProductAvailability').prefetch_related('images_set','Likes')\
    .annotate(comments_Count = Count('comments_post',distinct=True)).annotate(
        Count('Likes',distinct=True),is_liked=Exists(
        Post.Likes.through.objects.filter(
            post_id=OuterRef('pk'), user_id=user_id
        )
    ),isSaved=Exists(
        Post.favourites.through.objects.filter(
            post_id=OuterRef('pk'), user_id=user_id
        ))
        # ,
        # isFollowed=Exists(
        #     People.following.through.objects.filter(
        #         people_id=OuterRef('people_id'), user_id=user_id
        #     )
        # )
    ).all().order_by('-id')
    array = []
    for post in posts:
        if(post.user.people.following.through.objects.filter(people_id = post.user.people.id ,user_id=user_id).exists()):
            isFollowed = True
        else:
            isFollowed = False
        # if(post.Likes.filter(id=user_id).exists()):
        #     isLiked = True
        # else:
        #     isLiked = False
        IsSaved = False
        if(post.isSaved == True):
            IsSaved = 'Saved'
        else:
            IsSaved = 'Save'
        d={}
        if((datetime.now(timezone.utc) - post.Created_date).days > 7):
            created_date = str((datetime.now(timezone.utc) - post.Created_date).days) + ' days ago'
        else:
            created_date = post.Created_date.strftime("%d %b %Y")
        d = {
            'post_id':post.id,
            'user_id':post.user_id,
            'current_user_id':user_id,
            'title' : post.title,
            'description':post.description,
            'Tag1':post.Tag1,
            'Tag2':post.Tag2,
            'Tag3':post.Tag3,
            'Tag1_Name':post.Tag1_Name,
            'Tag2_Name':post.Tag2_Name,
            'Tag3_Name':post.Tag3_Name,
            'people_photo':post.user.people.photo,
            # 'category':post.category,
            'userName':post.user.username.capitalize(),
            'images' : post.images_set.all(),
            # 'comments' : post.comments_post.select_related().prefetch_related().all(),
            # 'comments_count': post.comments_post__count,
            'comments_count':post.comments_Count,
            'likesCount' : post.Likes__count,
            # 'actualLikeCount':post.likesCount(),
            # 'actualCommentCount':post.comments_post.count(),  
            # 'almost':post.Likes.count(),
            'isLiked':post.is_liked,
            'first_char':post.user.username[0].capitalize(),
            'product_availability':post.ProductAvailability,
            'created_at':created_date,
            'isSaved':post.isSaved,
            'IsSaved':IsSaved,
            'isFollowed':isFollowed
        }
        array.append(d)
    # print(array)
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
    # print(request.FILES)
    if(request.method == 'POST'):
        user_id = request.user.id
        title = request.POST.get('Ad-title')
        description = request.POST.get('Ad-Desc')
        # category = request.POST.get('category')
        ProductAvailability_id = request.POST.get('Product_available_at')
        Tag1 = request.POST.get('Tag1')
        Tag2 = request.POST.get('Tag2')
        Tag3 = request.POST.get('Tag3')
        Tag1_Name = request.POST.get('Tag1-Name')
        Tag2_Name = request.POST.get('Tag2-Name')
        Tag3_Name = request.POST.get('Tag3-Name')
        # category_d = Category.objects.get(id=category)
        ProductAvailability_model = ProductAvailability.objects.get(id=ProductAvailability_id)
        Ad = Post(user_id=user_id,title=title,description=description,ProductAvailability=ProductAvailability_model,Tag1=Tag1,Tag2=Tag2,Tag3=Tag3,Tag1_Name=Tag1_Name,Tag2_Name=Tag2_Name,Tag3_Name=Tag3_Name)
        Ad.save()
        Images_list = request.FILES.getlist('files')
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
        # 'post_Tags':post.Tags,
        # 'post_category':post.category,
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


@login_required(login_url='/members/login_me_in')
def search(request):
    if request.method == 'POST':
        search_text = request.POST.get('search_text')
        if(search_text != ''):
            search_results = Post.objects.filter(Q(title__icontains=search_text) | Q(description__icontains=search_text) | Q(Tags__icontains=search_text))
            print(search_results)
            return render(request, template_name='Search.html',context={'search_results':search_results})
        else:
            return redirect(request.META['HTTP_REFERER'])
    return render(request, template_name='Search.html')


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

@api_view()
def get_post_availablity(request):
    labels = ProductAvailability.objects.all()
    serializer = ProductAvailabilitySerializer(labels, many=True)
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


@api_view(['GET','POST'])
def HidePost(request):
    print(request)
    try:
        if(request.method == 'POST'):
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            post.users.add(request.user)
            return JsonResponse({"message":"Hidden","status": status.HTTP_200_OK})
        return JsonResponse({"message":"Not Allowed"})
    except:
        return JsonResponse({"message":"Something Went Wrong"})


@api_view(['GET','POST'])
def favouritePost(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        user_id = request.user.id
        post = Post.objects.get(id=post_id)
        if(post.favourites.filter(id=user_id).exists()):
            post.favourites.remove(user_id)
            return JsonResponse({"message":'Favourite Removed',"status":status.HTTP_200_OK,'id':post_id,'savestatus':'save'})
        else:
            post.favourites.add(user_id)
            return JsonResponse({"message":"Favourited","status": status.HTTP_200_OK,'id':post_id,'savestatus':'saved'})
    return JsonResponse({"message":"Not Allowed"})


@api_view(['GET','POST'])
def follow_user(request):
    if request.method == 'POST':
        follow_this_user_id = request.POST.get('user_id')
        current_user_id = request.user.id

        people = People.objects.get(user_id=follow_this_user_id)
        if(people.following.filter(id=current_user_id).exists()):
            people.following.remove(current_user_id)
            return JsonResponse({"message":'Unfollowed',"status":status.HTTP_200_OK,'id':follow_this_user_id,'followstatus':'follow'})
        else:
            people.following.add(current_user_id)
            return JsonResponse({"message":"Followed","status": status.HTTP_200_OK,'id':follow_this_user_id,'followstatus':'Unfollow'})



        # people = People.following.objects.get(id=follow_this_user_id)
        # if(people.following.filter(id=follow_this_user_id).exists()):
        #     people.following.remove(follow_this_user_id)
        #     return JsonResponse({"message":'Unfollowed',"status":status.HTTP_200_OK,'id':follow_this_user_id,'followstatus':'follow'})
        # else:
        #     people.following.add(follow_this_user_id)
        #     return JsonResponse({"message":"Followed","status": status.HTTP_200_OK,'id':follow_this_user_id,'followstatus':'followed'})
    return JsonResponse({"message":"Not Allowed"})