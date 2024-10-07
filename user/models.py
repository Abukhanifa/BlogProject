from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=2500)
    profile_pic = models.ImageField(blank=True, null=True)
    
    def __str__(self):
        return f'User: {self.user}, Bio: {self.bio}'
    
    
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Follower: {self.follower}, Following: {self.following}'
        