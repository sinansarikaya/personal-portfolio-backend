from django.urls import path
from .views import (
    BlogListView, BlogListCreate, BlogRetrieveUpdateDestroy,
    CategoryListView, CategoryListCreate, CategoryRetrieveUpdateDestroy
)

urlpatterns = [
    path('categorylist/', CategoryListView.as_view(), name='category_list'),
    path('categories/', CategoryListCreate.as_view(), name='category_list_create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category_retrieve_update_destroy'),
    path('categories/update/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category_update'),

    path('bloglist/', BlogListView.as_view(), name='blog_list'),
    path('blogs/', BlogListCreate.as_view(), name='blog_list_create'),
    path('blogs<int:pk>/', BlogRetrieveUpdateDestroy.as_view(), name='blog_retrieve_update_destroy'),
    path('blogs/update/<int:pk>/', BlogRetrieveUpdateDestroy.as_view(), name='blog_update'),
]


