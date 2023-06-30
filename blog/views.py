from rest_framework import generics, permissions
from .models import Blog, Category
from .serializers import BlogSerializer, CategorySerializer

class CategoryListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BlogListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class FixBlogDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogDetailEn(FixBlogDetail):
    lookup_field = 'slug_en'

class BlogDetailTr(FixBlogDetail):
    lookup_field = 'slug_tr'

class BlogDetailNo(FixBlogDetail):
    lookup_field = 'slug_no'

class CategoryDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BlogUpdate(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogDelete(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class CategoryAdminOps(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
