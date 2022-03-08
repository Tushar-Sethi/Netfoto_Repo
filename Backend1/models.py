from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    Created_By = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,null=True)
    Created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)   
    description = models.CharField(max_length=1000,null=True)
    Tags = models.CharField(max_length = 255,null=True,blank=True)
    Created_date = models.DateTimeField(auto_now_add=True)
    Updated_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    Likes = models.ManyToManyField(to=User, related_name='Post_likes')
    favourites = models.ManyToManyField(to=User,blank=True,related_name="favourite")

    def __str__(self):
        return self.title

    def likesCount(self):
        return self.Likes.count()

    def get_absolute_url(self):
        #return reverse('Blog_Details', args=(str(self.id)))   # to return to the specific blog post details 
        return reverse('home') 

class People(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_pics', blank=True,null=True)
    Phone_number = models.CharField(max_length=255,null=True,blank=True)
    Birth_Date = models.DateField(null=True,blank=True)
    Created_date = models.DateTimeField(auto_now_add=True)
    Updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class Images(models.Model):
    Post = models.ForeignKey(Post,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/')
    # Tag1 = models.CharField(max_length=255,null=True,blank=True)
    # Tag2 = models.CharField(max_length=255,null=True,blank=True)
    # Tag3 = models.CharField(max_length=255,null=True,blank=True)


class Comment(models.Model):
    comment = models.TextField(null=True)
    Created_date = models.DateTimeField(auto_now_add=True)
    Updated_date = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments_post')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_user')

    def __str__(self):
        return self.comment


