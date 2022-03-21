from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    Created_By = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,null=True)
    Created_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.title

class ProductAvailability(models.Model):
    title = models.CharField(max_length=255,null=True)
    Created_date = models.DateTimeField(auto_now_add=True)
    Updated_date = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.title

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # category = models.ForeignKey(Category, on_delete=models.PROTECT)
    ProductAvailability = models.ForeignKey(ProductAvailability, on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(max_length=255,null=True)   
    description = models.CharField(max_length=1000,null=True)
    Likes = models.ManyToManyField(to=User, related_name='Post_likes')
    favourites = models.ManyToManyField(to=User,blank=True,related_name="favourite")
    Tag1 = models.CharField(max_length=255,null=True,blank=True)
    Tag2 = models.CharField(max_length=255,null=True,blank=True)
    Tag3 = models.CharField(max_length = 255, null = True, blank = True)
    Tag1_Name = models.CharField(max_length=255,null=True,blank=True)
    Tag2_Name = models.CharField(max_length=255,null=True,blank=True)
    Tag3_Name = models.CharField(max_length=255,null=True,blank=True)
    users = models.ManyToManyField(User, related_name='users_hidden_from_post')
    Created_date = models.DateTimeField(auto_now_add=True)
    Updated_date = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.title

    def likesCount(self):
        return self.Likes.count()

    def get_absolute_url(self):
        #return reverse('Blog_Details', args=(str(self.id)))   # to return to the specific blog post details 
        return reverse('home') 

class People(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='people')
    Name = models.CharField(max_length=255,null=True)
    # email = models.EmailField(max_length=255,null=False,unique=True,blank=False)
    is_verified = models.BooleanField(default=False)
    OTP = models.CharField(max_length=6, null=True, blank=True)
    following = models.ManyToManyField(to=User, related_name='following', blank=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True,null=True)
    Phone_number = models.CharField(max_length=255,null=True,blank=True)
    Birth_Date = models.DateField(null=True,blank=True)
    Created_date = models.DateTimeField(auto_now_add=True)
    Updated_date = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.user.email


class Images(models.Model):
    Post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')


class Comment(models.Model):
    comment = models.TextField(null=True)
    Created_date = models.DateTimeField(auto_now_add=True)
    Updated_date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_user')

    def __str__(self):
        return self.comment




