from rest_framework import serializers
from .models import Blog, Category

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
