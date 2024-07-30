from typing import Iterable
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from tinymce.models import HTMLField


class CustomUser(AbstractUser):
    username = models.CharField(max_length=222, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    joined_at = models.DateTimeField(default=timezone.now, editable=False)

    REQUIRED_FIELDS = ['username', ]
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_profile.png')
    name = models.CharField(max_length=222, null=True, blank=True)
    bio = models.TextField(null=True,  blank=True)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        if self.name:
            return f"{self.name}"
        
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} {self.post}"
    
class Topic(models.Model):
    name = models.CharField(max_length=200)


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')

    def __str__(self) -> str:
        return f"{self.user.username}"

    
class Share(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='shares')
    shared_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ('user', 'post')

    def str(self):
        return f'{self.user.username}'

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='', null=True, blank=True)
    text = HTMLField(null=False, blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    updated_at =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.text}"
        
    class Meta:
        ordering = ['-updated_at', '-created_at']

    @property
    def users_liked(self):
        result = []
        for i in self.likes.all():
            result.append(int(i.user.id))
        return result


class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower}"
    


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(CustomUser, related_name='receiver', on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}"