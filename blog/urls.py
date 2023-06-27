from django.urls import path
from .views import (
    BlogListView, BlogUpdate, BlogDelete, BlogCreate, BlogDetail,
    CategoryListView, CategoryAdminOps, CategoryCreate, CategoryDetail
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'), 
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category_detail'),
    path('category/create/', CategoryCreate.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryAdminOps.as_view(), name='category_admin_ops'),

    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<slug:slug>/', BlogDetail.as_view(), name='blog_detail'),
    path('blog_create/', BlogCreate.as_view(), name='blog_create'),
    path('blog_update/<int:pk>/', BlogUpdate.as_view(), name='blog_update'),
    path('blog_delete/<int:pk>/', BlogDelete.as_view(), name='blog_delete'),
]
