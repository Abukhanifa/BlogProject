from django.contrib import admin
from user.models import Profile, Follow


@admin.register(Profile)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio',)
    search_fields = ('bio',)
    
    
@admin.register(Follow)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')
    search_fields = ('follower',)

