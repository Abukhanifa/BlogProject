from django.contrib import admin
from blog.models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)
    search_fields = ('title',)
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author',)
    search_fields = ('author',)
