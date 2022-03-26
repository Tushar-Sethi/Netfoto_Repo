from rest_framework import serializers

class PostSerializer(serializers.Serializer):
    
    # user = serializers.ForeignKey(User, on_delete=models.PROTECT)
    title = serializers.CharField(max_length=255)   
    description = serializers.CharField(max_length=255)
    # Post_image = serializers.ImageField(upload_to='media/',null=True)
    # Created_date = serializers.DateTimeField(auto_now_add=True)
    # Updated_date = serializers.DateTimeField(auto_now=True)

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=255)

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)

class ProductAvailabilitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)

class peopleSerializer(serializers.Serializer):
    OTP = serializers.CharField(max_length=6)
    Name = serializers.CharField(max_length=255)
    photo = serializers.ImageField()


class commentsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    comment = serializers.CharField(max_length=255)
    user = UserSerializer()
    post = PostSerializer()
    Created_date = serializers.DateTimeField()
    people = peopleSerializer(source='user.people')

