from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Blog, Category, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email']

class BlogTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title_en']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

    category = CategorySerializer(read_only=True)

    category_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)
        return Blog.objects.create(category=category, **validated_data)
    

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    blog = BlogTitleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'blog', 'text', 'created_at', 'updated_at', 'visible'] 


