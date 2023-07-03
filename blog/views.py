from rest_framework import generics, permissions
from .models import Blog, Category, Comment
from .serializers import BlogSerializer, CategorySerializer, CommentSerializer

class CategoryFixView():
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryListView(CategoryFixView, generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

class CategoryAdminOps(CategoryFixView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]

class CategoryCreate(CategoryFixView, generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]

class CategoryDetail(CategoryFixView, generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]

class FixBlogDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class BlogListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    page_size = 1

class BlogDetailEn(FixBlogDetail):
    lookup_field = 'slug_en'

class BlogDetailTr(FixBlogDetail):
    lookup_field = 'slug_tr'

class BlogDetailNo(FixBlogDetail):
    lookup_field = 'slug_no'

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

class CommentFixView():
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentListView(CommentFixView, generics.ListAPIView):
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Comment.objects.select_related('user', 'blog').all()

class CommentCreateView(CommentFixView, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

class CommentDetailUpdateDeleteView(CommentFixView, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
