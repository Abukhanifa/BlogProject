from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField(max_length=2500)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Title: {self.title}, Content: {self.content}'
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = 'Posts'
        
        
class Comment(models.Model):
    content = models.TextField(max_length=2500)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Content: {self.content}'
    
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = 'Comments'