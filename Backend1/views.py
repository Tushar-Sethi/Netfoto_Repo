from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.admin import User
from .models import Post, Category, People, Images, Comment, ProductAvailability, Stage1, product_details,product_orders
from django.urls import reverse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer, CategorySerializer, ProductAvailabilitySerializer, UserSerializer, commentsSerializer, peopleSerializer
from django.db.models import Count, Exists, OuterRef, Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import status
from datetime import datetime, timezone
import threading
import random
import string


@login_required(login_url='/members/first/')
def index(request):
    user_id = request.user.id
    posts = Post.objects.exclude(users=request.user)\
        .select_related('user__people', 'ProductAvailability').prefetch_related('images_set', 'Likes')\
        .annotate(comments_Count=Count('comments_post', distinct=True)).annotate(
        Count('Likes', distinct=True), is_liked=Exists(
            Post.Likes.through.objects.filter(
                post_id=OuterRef('pk'), user_id=user_id
            )
        ), isSaved=Exists(
            Post.favourites.through.objects.filter(
                post_id=OuterRef('pk'), user_id=user_id
            )),
    ).all().order_by('-id')
    array = []
    for post in posts:
        if(post.user.people.following.through.objects.filter(people_id=post.user.people.id, user_id=user_id).exists()):
            isFollowed = True
        else:
            isFollowed = False
        IsSaved = False
        if(post.isSaved == True):
            IsSaved = 'Saved'
        else:
            IsSaved = 'Save'
        d = {}
        if((datetime.now(timezone.utc) - post.Created_date).days > 7):
            created_date = str(
                (datetime.now(timezone.utc) - post.Created_date).days) + ' days ago'
        else:
            created_date = post.Created_date.strftime("%d %b %Y")

        if(post.Tag1 != ''):
            tag1 = post.Tag1
        else:
            tag1 = None

        if(post.Tag2 != ''):
            tag2 = post.Tag2
        else:
            tag2 = None

        if(post.Tag3 != ''):
            tag3 = post.Tag3
        else:
            tag3 = None
        d = {
            'post_id': post.id,
            'user_id': post.user_id,
            'current_user_id': user_id,
            'title': post.title,
            'description': post.description,
            'Tag1': tag1,
            'Tag2': tag2,
            'Tag3': tag3,
            'Tag1_Name': post.Tag1_Name,
            'Tag2_Name': post.Tag2_Name,
            'Tag3_Name': post.Tag3_Name,
            'people_photo': post.user.people.photo,
            'userName': post.user.username.capitalize(),
            'images': post.images_set.all(),
            'comments_count': post.comments_Count,
            'likesCount': post.Likes__count,
            'isLiked': post.is_liked,
            'first_char': post.user.username[0].capitalize(),
            'product_availability': post.ProductAvailability,
            'created_at': created_date,
            'isSaved': post.isSaved,
            'IsSaved': IsSaved,
            'isFollowed': isFollowed,
        }
        array.append(d)
    return render(request, template_name='index.html', context={'post': array})


def demo(request):
    user = request.user
    username = user.username
    people = People.objects.get(user__username=username)
    return render(request, template_name='Demo.html')


@login_required(login_url='/members/first/')
def demo2(request):
    user_id = request.user.id
    posts = Post.objects.exclude(users=request.user)\
        .select_related('user__people', 'ProductAvailability').prefetch_related('images_set', 'Likes')\
        .annotate(comments_Count=Count('comments_post', distinct=True)).annotate(
        Count('Likes', distinct=True), is_liked=Exists(
            Post.Likes.through.objects.filter(
                post_id=OuterRef('pk'), user_id=user_id
            )
        ), isSaved=Exists(
            Post.favourites.through.objects.filter(
                post_id=OuterRef('pk'), user_id=user_id
            )),
    ).all().order_by('-id')
    array = []
    count = 0
    for post in posts:
        if(post.user.people.following.through.objects.filter(people_id=post.user.people.id, user_id=user_id).exists()):
            isFollowed = True
        else:
            isFollowed = False
        IsSaved = False
        if(post.isSaved == True):
            IsSaved = 'Saved'
        else:
            IsSaved = 'Save'
        d = {}
        if((datetime.now(timezone.utc) - post.Created_date).days > 7):
            created_date = str(
                (datetime.now(timezone.utc) - post.Created_date).days) + ' days ago'
        else:
            created_date = post.Created_date.strftime("%d %b %Y")

        if(post.Tag1 != ''):
            tag1 = post.Tag1
        else:
            tag1 = None

        if(post.Tag2 != ''):
            tag2 = post.Tag2
        else:
            tag2 = None

        if(post.Tag3 != ''):
            tag3 = post.Tag3
        else:
            tag3 = None
        d = {
            'post_id': post.id,
            'user_id': post.user_id,
            'current_user_id': user_id,
            'title': post.title,
            'description': post.description,
            'Tag1': tag1,
            'Tag2': tag2,
            'Tag3': tag3,
            'Tag1_Name': post.Tag1_Name,
            'Tag2_Name': post.Tag2_Name,
            'Tag3_Name': post.Tag3_Name,
            'people_photo': post.user.people.photo,
            'userName': post.user.username.capitalize(),
            'images': post.images_set.all(),
            'comments_count': post.comments_Count,
            'likesCount': post.Likes__count,
            'isLiked': post.is_liked,
            'first_char': post.user.username[0].capitalize(),
            'product_availability': post.ProductAvailability,
            'created_at': created_date,
            'isSaved': post.isSaved,
            'IsSaved': IsSaved,
            'isFollowed': isFollowed,
        }
        array.append(d)
        count = count + 1
    return render(request, template_name='Demo2.html', context={'post': array, 'count': count})


@login_required(login_url='/members/first/')
def Create_a_Post(request):
    return render(request, template_name='Create_a_Post.html')


@login_required(login_url='/members/first/')
def Save_Post_TO_DB(request):
    if(request.method == 'POST'):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        people = People.objects.get(user_id=user_id)
        title = request.POST.get('Ad-title')
        description = request.POST.get('Ad-Desc')
        ProductAvailability_id = request.POST.get('Product_available_at')
        Tag1 = request.POST.get('Tag1')
        Tag2 = request.POST.get('Tag2')
        Tag3 = request.POST.get('Tag3')
        Tag1_Name = request.POST.get('Tag1-Name')
        Tag2_Name = request.POST.get('Tag2-Name')
        Tag3_Name = request.POST.get('Tag3-Name')
        product_details = request.POST.get('product_details')
        ProductAvailability_model = ProductAvailability.objects.get(
            id=ProductAvailability_id)
        Ad = Post(user_id=user_id, title=title, description=description, ProductAvailability=ProductAvailability_model, Tag1=Tag1,
                  Tag2=Tag2, Tag3=Tag3, Tag1_Name=Tag1_Name, Tag2_Name=Tag2_Name, Tag3_Name=Tag3_Name, product_details=product_details)
        Ad.save()
        Images_list = request.FILES.getlist('files')
        for Image in Images_list:
            Img = Images(Post=Ad, image=Image)
            Img.save()
        people.step_2 = True
        people.save()
        return redirect('/')
    return render(request, template_name='index.html')


@login_required(login_url='/members/first/')
def SpecificUser(request, pk):
    user_id = pk
    user_PEOPLE_ID = People.objects.get(user_id=user_id).id
    current_user_id = request.user.id
    person = People.objects.select_related('user').get(user_id=user_id)
    user_Ads = Post.objects.prefetch_related(
        'images_set').filter(user_id=user_id).all()
    saved_post = Post.objects.filter(favourites=user_id)
    Liked = Post.objects.filter(Likes=user_id)
    isFollowed = People.following.through.objects.filter(
        people_id=user_PEOPLE_ID, user_id=current_user_id).exists()
    context = {
        'user_id': user_id,
        'username': person.user.username.capitalize(),
        'people_photo': person.photo,
        'saved': saved_post,
        'Liked': Liked,
        'followers': person.following.all(),
        'following': People.objects.filter(following=user_id).all(),
        'person': person,
        'user_Ads': user_Ads,
        'first_char': person.user.username[0].capitalize(),
        'current_user_id': current_user_id,
        'isFollowed': isFollowed,
    }
    return render(request, template_name='Specific_User_Page.html', context={'Data': context})


def view_post(request, pk):
    
    post_id = pk
    post = Post.objects.select_related().prefetch_related(
        'images_set', 'comments_post', 'comments_post__user').get(id=post_id)
    
    
    people = People.objects.select_related().get(user_id=post.user_id)
    context = {
        'post_id': post.id,
        'post_title': post.title,
        'post_description': post.description,
    
    
        'post_UserId': post.user_id,
        'post_userName': post.user.username,
        'post_images': post.images_set.all(),
        'post_comments': post.comments_post.all(),
        'total_comments': post.comments_post.count(),
        'post_likesCount': post.likesCount(),
        'people': people,
        'first_char': people.user.username[0].capitalize()
    }
    
    return render(request, template_name='View_Post.html', context={'post_details': context})


@login_required(login_url='/members/first/')
def favourite_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if(post.favourites.filter(id=request.user.id).exists()):
            post.favourites.remove(request.user)
        else:
            post.favourites.add(request.user)
    else:
        return redirect('members/login_me_in')
    return redirect(request.META['HTTP_REFERER'])
    


@login_required(login_url='/members/first/')
def comment_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        comment = request.POST.get('comment')
        if(comment != ''):
            Comment.objects.create(post=post, user=user, comment=comment)
        return redirect(request.META['HTTP_REFERER'])
    return render(request, template_name='index.html')


@login_required(login_url='/members/first/')
def search(request):
    if(request.user.is_authenticated):
        if request.method == 'POST':
            search_text = request.POST.get('search_text')
            if(search_text != ''):
                user_id = request.user.id
                search_results = Post.objects.filter(Q(title__icontains=search_text) | Q(description__icontains=search_text) | Q(product_details__icontains=search_text))\
                    .select_related('user__people', 'ProductAvailability').prefetch_related('images_set', 'Likes')\
                    .annotate(comments_Count=Count('comments_post', distinct=True)).annotate(
                    Count('Likes', distinct=True), is_liked=Exists(
                        Post.Likes.through.objects.filter(
                            post_id=OuterRef('pk'), user_id=user_id
                        )
                    ), isSaved=Exists(
                        Post.favourites.through.objects.filter(
                            post_id=OuterRef('pk'), user_id=user_id
                        )),
                    isFollowed1=Exists(
                        People.objects.filter(
                            following__post__id=OuterRef('pk'), user_id=user_id
                        )
                    )).all().order_by('-id')
                array = []
                for post in search_results:
                    if(post.user.people.following.through.objects.filter(people_id=post.user.people.id, user_id=user_id).exists()):
                        isFollowed = True
                    else:
                        isFollowed = False
                    IsSaved = False
                    if(post.isSaved == True):
                        IsSaved = 'Saved'
                    else:
                        IsSaved = 'Save'
                    d = {}
                    if((datetime.now(timezone.utc) - post.Created_date).days > 7):
                        created_date = str(
                            (datetime.now(timezone.utc) - post.Created_date).days) + ' days ago'
                    else:
                        created_date = post.Created_date.strftime("%d %b %Y")

                    if(post.Tag1 != ''):
                        tag1 = post.Tag1
                    else:
                        tag1 = None

                    if(post.Tag2 != ''):
                        tag2 = post.Tag2
                    else:
                        tag2 = None

                    if(post.Tag3 != ''):
                        tag3 = post.Tag3
                    else:
                        tag3 = None
                    d = {
                        'post_id': post.id,
                        'user_id': post.user_id,
                        'current_user_id': user_id,
                        'title': post.title,
                        'description': post.description,
                        'Tag1': tag1,
                        'Tag2': tag2,
                        'Tag3': tag3,
                        'Tag1_Name': post.Tag1_Name,
                        'Tag2_Name': post.Tag2_Name,
                        'Tag3_Name': post.Tag3_Name,
                        'people_photo': post.user.people.photo,
                        
                        'userName': post.user.username.capitalize(),
                        'images': post.images_set.all(),
                        
                        
                        'comments_count': post.comments_Count,
                        'likesCount': post.Likes__count,
                        
                        'isLiked': post.is_liked,
                        'first_char': post.user.username[0].capitalize(),
                        'product_availability': post.ProductAvailability,
                        'created_at': created_date,
                        'isSaved': post.isSaved,
                        'IsSaved': IsSaved,
                        'isFollowed': isFollowed,
                        'isFollowed1': post.isFollowed1,
                    }
                    array.append(d)
                return render(request, template_name='SearchResults.html', context={'post': array, 'search_text': search_text})
            else:
                return redirect(request.META['HTTP_REFERER'])
        return render(request, template_name='Search.html')
    else:
        return redirect('members/login_me_in')


def Liked_posts(request, pk):
    user_id = pk
    post = Post.objects.filter(Likes__id=user_id).all()
    return render(request, template_name='LikedPosts.html', context={'post': post})


def saved_posts(request, pk):
    user_id = pk
    post = Post.objects.filter(favourites__id=user_id).all()
    return render(request, template_name='SavedPosts.html', context={'post': post})


def followers(request, pk):
    user_id = pk
    user = get_object_or_404(User, pk=user_id)
    people = user.people
    followers = people.following.all()
    return render(request, template_name='followersList.html', context={'followers': followers})


def following(request, pk):
    user_id = pk
    user = get_object_or_404(User, pk=user_id)
    people = user.people
    following = People.objects.filter(following=user_id).all()
    return render(request, template_name='followingList.html', context={'following': following})


def getFreePhotos(request):
    return render(request, template_name='FreePhotos.html')


@login_required(login_url='/members/first/')
def getFreePhotographs(request):
    if(request.user.is_authenticated):
        user_id = request.user.id
        user = get_object_or_404(User, pk=user_id)
        people = user.people
        if(people.step_3 == True):
            return redirect('come_back_later')
        if request.method == 'POST':
            if(people.step_1 == False):
                company_name = request.POST.get('Company_Name')
                GST = request.POST.get('GST')
                company_address1 = request.POST.get('Company_Address1')
                company_address2 = request.POST.get('Company_Address2')
                City = request.POST.get('City')
                State = request.POST.get('State')
                pincode = request.POST.get('Pincode')
                About = request.POST.get('About')
                ValidateCompany.objects.create(user=user, Company_Name=company_name, GST_number=GST, Company_Address1=company_address1,
                                               Company_Address2=company_address2, City=City, State=State, pinCode=pincode, About=About)
                people.step_1 = True
                people.save()
                post = Post.objects.filter(user_id=user_id).exists()
                if(post == True):
                    return redirect('Another_Post_or_Not')
                return redirect('unlock_free_photos_post_ad')
            else:
                post = Post.objects.filter(user_id=user_id).exists()
                if(post == True):
                    return redirect('Another_Post_or_Not')
                # Go to Step 2','step 2 code goes here','i.e other Questions
                return redirect('unlock_free_photos_post_ad')
        if(people.step_1 == True):
            post = Post.objects.filter(user_id=user_id).exists()
            if(post == True):
                return redirect('Another_Post_or_Not')
            return redirect('unlock_free_photos_post_ad')
        return render(request, template_name='FreePhotograph.html')
    return redirect('members/login_me_in')

@login_required(login_url='/members/first/')
def getFreePhotograph(request):
    if(request.user.is_authenticated):
        user_id = request.user.id
        user = get_object_or_404(User, pk=user_id)
        people = user.people
        stage = people.stages.split(',')[-1]
        if(request.method == 'POST'):
            if(stage != ''):
                if(stage == '1'):
                    print('Stage2')
                elif(stage == '2'):
                    print('stage3')
                #other code goes here

            else:
                company_name = request.POST.get('Company_Name')
                GST = request.POST.get('GST')
                company_address1 = request.POST.get('Company_Address1')
                company_address2 = request.POST.get('Company_Address2')
                City = request.POST.get('City')
                State = request.POST.get('State')
                pincode = request.POST.get('Pincode')
                About = request.POST.get('About')
                Stage1(user=user, 
                    Company_Name = company_name, 
                    GST_number = GST, 
                    Company_Address1 = company_address1,
                    Company_Address2 = company_address2,
                    City = City,
                    State = State,
                    pinCode = pincode,
                    About = About
                    ).save()
            people.step_1 = True
            people.save()
            if(people.step_2 == False):
                return redirect('unlock_free_photos_post_ad')
            return redirect('Another_Post_or_Not')
        else:
            if(people.step_3 == True):
                return redirect('come_back_later')
            else:
                if(people.step_1 == True):
                    if(people.step_2 == True):
                        return redirect("photography_order_details")
                    else:
                        return redirect("unlock_free_photos_post_ad")
                else:
                    if(stage != ''):
                        if(stage == "1"):
                            return render(request, template_name='Stage2.html')
                        elif(stage == "2"):
                            return render(request, template_name='Stage3.html')
                        #other code goes here
                    else:
                        return render(request, template_name='Stage1.html')
                
    # return redirect('members/login_me_in')

def unlock_free_photos_post_ad(request):
    if(request.user.is_authenticated):
        user_id = request.user.id
        user = get_object_or_404(User, pk=user_id)
        people = user.people
        if(people.step_1 == False):
            return redirect('Free_photograph_form')
        if request.method == 'POST':
            title = request.POST.get('Ad-title')
            description = request.POST.get('Ad-Desc')
            ProductAvailability_id = request.POST.get('Product_available_at')
            Tag1 = request.POST.get('Tag1')
            Tag2 = request.POST.get('Tag2')
            Tag3 = request.POST.get('Tag3')
            Tag1_Name = request.POST.get('Tag1-Name')
            Tag2_Name = request.POST.get('Tag2-Name')
            Tag3_Name = request.POST.get('Tag3-Name')
            product_details = request.POST.get('product_details')
            ProductAvailability_model = ProductAvailability.objects.get(
                id=ProductAvailability_id)
            Ad = Post(user_id=user_id, title=title, description=description, ProductAvailability=ProductAvailability_model, Tag1=Tag1,
                      Tag2=Tag2, Tag3=Tag3, Tag1_Name=Tag1_Name, Tag2_Name=Tag2_Name, Tag3_Name=Tag3_Name, product_details=product_details)
            Ad.save()
            Images_list = request.FILES.getlist('files')
            for Image in Images_list:
                Img = Images(Post=Ad, image=Image)
                Img.save()
            people.step_2 = True
            people.save()
            return redirect('photography_order_details')
        if(people.step_2 == True):
            return redirect('Another_Post_or_Not')
        return render(request, template_name='Unlock_free_photos_create_post.html')
    return redirect('members/login_me_in')


def order_details(request):
    if(request.user.is_authenticated):
        user_id = request.user.id
        user = get_object_or_404(User, pk=user_id)
        people = user.people
        if(request.method == 'POST'):
            if(people.step_1 == False):
                # messages.error(request, 'Please fill the essential Information')
                return redirect('Free_photograph_form')
            if(people.step_2 == False):
                # messages.error(request, 'Please add one post to continue')
                return redirect('unlock_free_photos_post_ad')
            product_name = request.POST.get('product-name')
            no_of_products = request.POST.get('select')
            no_of_views = request.POST.get('select_view')
            how_sending_products = request.POST.get('send_products_name')
            send_products_back = request.POST.get('send_products_back_name')
            additional_specifications = request.POST.get(
                'specifications_product_photography')
            PD = product_details(people=people, Product_Name=product_name, no_of_products=no_of_products, no_of_views=no_of_views,
                                 send_products=how_sending_products, send_products_back=send_products_back, product_additional_specifications=additional_specifications)
            PD.save()
            order_ID = ran_gen(8)
            Order = product_orders(people_id = people.id, orderID=order_ID)
            Order.save()
            people.step_3 = True
            stage = people.stages
            if(people.stages == ''):
                people.stages = '1'
            else:
                stage = stage.split(',')
                last_stage = stage[-1]
                next_stage = str(int(last_stage) + 1)
                stage.append(next_stage)
                listToStr = ','.join(map(str, stage))
                people.stages = listToStr
            people.save()
            return redirect('photography_order_confirmed')
        else:
            if(people.step_1 == False):
                return redirect('Free_photograph_form')
            if(people.step_2 == False):
                return redirect('unlock_free_photos_post_ad')
            if(people.step_3 == True):
                return redirect('come_back_later')
            else:
                return render(request, template_name='Order_details.html')
    return redirect('members/login_me_in')

@login_required(login_url='members/login_me_in')
def order_confirmed(request):
    if(request.user.is_authenticated):
        user_id = request.user.id
        user = get_object_or_404(User, pk=user_id)
        people = user.people
        if(people.step_1 == False):
            return redirect('Free_photograph_form')
        if(people.step_2 == False):
            return redirect('unlock_free_photos_post_ad')
        if(people.step_3 == False):
            return redirect('order_details')
        PD = product_details.objects.filter(people=people).all().order_by('-id')[0]
        Order = product_orders.objects.filter(people_id=people.id).all().order_by('-id')[0]
        return render(request, template_name='Order_confirmed.html', context={'PD': PD, 'Order': Order})
    return redirect('members/login_me_in')


def come_back_later(request):

    return render(request, template_name='Come_back_later.html')


def Another_Post_or_Not(request):
    return render(request, template_name='Another_Post_or_Not.html')


def ran_gen(size, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


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
        comment_obj = Comment(
            user_id=user_id, post_id=post_id, comment=comment)
        comment_obj.save()
        return Response('Comment Captured')
    return Response('Something Went Wrong. Error !! ')


@api_view(['GET', 'POST'])
def like_post(request):
    try:
        if(request.method == 'POST'):
            post_id = request.POST.get('post_id')
            user_id = request.user.id
            post = Post.objects.get(id=post_id)
            if(post.Likes.filter(id=user_id).exists()):
                post.Likes.remove(user_id)
                likesCount = post.Likes.count()
                return JsonResponse({"message": 'Like Removed', "status": status.HTTP_200_OK, 'id': post_id, 'likesCount': likesCount})
            else:
                post.Likes.add(user_id)
                likesCount = post.Likes.count()
                return JsonResponse({"message": "Liked", "status": status.HTTP_200_OK, 'id': post_id, 'likesCount': likesCount})
        return JsonResponse({"message": "Not Allowed"})
    except:
        return JsonResponse({"message": "Something Went Wrong"})


@api_view(['GET', 'POST'])
def HidePost(request):
    print(request)
    try:
        if(request.method == 'POST'):
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            post.users.add(request.user)
            return JsonResponse({"message": "Hidden", "status": status.HTTP_200_OK})
        return JsonResponse({"message": "Not Allowed"})
    except:
        return JsonResponse({"message": "Something Went Wrong"})


@api_view(['GET', 'POST'])
def favouritePost(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        user_id = request.user.id
        post = Post.objects.get(id=post_id)
        if(post.favourites.filter(id=user_id).exists()):
            post.favourites.remove(user_id)
            return JsonResponse({"message": 'Favourite Removed', "status": status.HTTP_200_OK, 'id': post_id, 'savestatus': 'save'})
        else:
            post.favourites.add(user_id)
            return JsonResponse({"message": "Favourited", "status": status.HTTP_200_OK, 'id': post_id, 'savestatus': 'saved'})
    return JsonResponse({"message": "Not Allowed"})


@api_view(['GET', 'POST'])
def follow_user(request):
    if request.method == 'POST':
        follow_this_user_id = request.POST.get('user_id')
        current_user_id = request.user.id
        people = People.objects.get(user_id=follow_this_user_id)

        if(people.following.filter(id=current_user_id).exists()):
            people.following.remove(current_user_id)
            return JsonResponse({"message": 'Unfollowed', "status": status.HTTP_200_OK, 'id': follow_this_user_id, 'followstatus': 'follow'})
        else:
            people.following.add(current_user_id)
            return JsonResponse({"message": "Followed", "status": status.HTTP_200_OK, 'id': follow_this_user_id, 'followstatus': 'Unfollow'})
    return JsonResponse({"message": "Not Allowed"})


@api_view(['GET'])
def get_comments(request):
    if request.method == 'GET':
        post_id = request.GET.get('post_id')
        comments = Comment.objects.filter(post_id=post_id).select_related(
            'user', 'post', 'user__people').order_by('-Created_date')[:2]
        serializer = commentsSerializer(comments, many=True)

        total_comments = Comment.objects.filter(post_id=post_id).count()
        print(total_comments)

        return Response({'comments': serializer.data, 'status': status.HTTP_200_OK, 'id': post_id, 'total_comments': total_comments})
    return Response({"message": "Not Allowed"})
