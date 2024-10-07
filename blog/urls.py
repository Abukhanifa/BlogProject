from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('posts/', views.posts, name='post_list'),
    path('post_create/', views.post_new, name='post'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),  
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),  
]
