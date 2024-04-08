from django.contrib import admin
from .models import Note, Photo


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["title"]

    def __str__(self):
        return Note.title

    class Meta:
        ordering = ["-pk"]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
