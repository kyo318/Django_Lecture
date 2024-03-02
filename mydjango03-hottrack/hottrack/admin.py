from django.contrib import admin
from .models import Song
from .utils.melon import get_likes_dict


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    search_fields = ["name", "artist_name", "album_name"]
    list_display = [
        "cover_image_tag",
        "name",
        "artist_name",
        "album_name",
        "genre",
        "like_count",
        "release_date",
    ]
    list_filter = ["genre"]
    actions = ["update_like_count"]

    def update_like_count(self, request, queryset):
        melon_uid_list = queryset.values_list("melon_uid", flat=True)
        likes_dict = get_likes_dict(melon_uid_list)

        for song in queryset:
            song.like_count = likes_dict[song.melon_uid]
        Song.objects.bulk_update(queryset, fields=["like_count"])

        self.message_user(request, "좋아요 갱신 완료")
