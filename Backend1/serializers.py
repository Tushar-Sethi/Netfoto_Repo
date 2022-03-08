from rest_framework import serializers

class PostSerializer(serializers.Serializer):
    
    # user = serializers.ForeignKey(User, on_delete=models.PROTECT)
    title = serializers.CharField(max_length=255)   
    description = serializers.CharField(max_length=255)
    # Post_image = serializers.ImageField(upload_to='media/',null=True)
    # Created_date = serializers.DateTimeField(auto_now_add=True)
    # Updated_date = serializers.DateTimeField(auto_now=True)

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)