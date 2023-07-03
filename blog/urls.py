from django.urls import path
from .views import (
    BlogListView, BlogUpdate, BlogDelete, BlogCreate, BlogDetailEn, BlogDetailTr, BlogDetailNo,
    CategoryListView, CategoryAdminOps, CategoryCreate, CategoryDetail,
    CommentListView, CommentCreateView, CommentDetailUpdateDeleteView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'), 
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category_detail'),
    path('category/create/', CategoryCreate.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryAdminOps.as_view(), name='category_admin_ops'),

    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blog_detail/en/<slug:slug_en>/', BlogDetailEn.as_view(), name='blog_detail_en'),
    path('blog_detail/tr/<slug:slug_tr>/', BlogDetailTr.as_view(), name='blog_detail_tr'),
    path('blog_detail/no/<slug:slug_no>/', BlogDetailNo.as_view(), name='blog_detail_no'),
    path('blog_create/', BlogCreate.as_view(), name='blog_create'),
    path('blog_update/<int:pk>/', BlogUpdate.as_view(), name='blog_update'),
    path('blog_delete/<int:pk>/', BlogDelete.as_view(), name='blog_delete'),

    path('comments/', CommentListView.as_view(), name='comment_list'),
    path('comment_create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/', CommentDetailUpdateDeleteView.as_view(), name='comment_detail_update_delete'),
]
