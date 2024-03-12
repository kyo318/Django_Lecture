from django.contrib import admin
from django.http import HttpRequest
from .models import Post, Article, Comment
from django.contrib.admin import (
    TabularInline,
    StackedInline,
)

from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline


class CommentTabularInline(GenericTabularInline):
    model = Comment
    fields = ["message", "rating"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request: HttpRequest, obj: None) -> bool:
        return False


class CommentStackedInline(GenericStackedInline):
    model = Comment
    fields = ["message", "rating"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentTabularInline]
