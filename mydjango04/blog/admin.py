from django.contrib import admin
from .models import Post, Comment, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class PostAdmin(admin.ModelAdmin):
    pass
