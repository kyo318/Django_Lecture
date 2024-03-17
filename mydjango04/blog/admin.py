from django.contrib import admin
from .models import Memo, MemoGroup, Post, Comment, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class PostAdmin(admin.ModelAdmin):
    pass


class MemoTabularInline(admin.TabularInline):
    model = Memo
    fields = ["message", "status"]


@admin.register(MemoGroup)
class MemoGroupAdmin(admin.ModelAdmin):
    inlines = [MemoTabularInline]
