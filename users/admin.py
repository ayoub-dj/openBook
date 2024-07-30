from django.contrib import admin

from .models import (
    CustomUser,
    Post,
    Comment,
    Topic,
    Like,
    Profile,
    Follow,
    Share,
    Message,
)

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Topic)
admin.site.register(Like)
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Share)
admin.site.register(Message)
