import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
# from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
# from django.db import connection
from django.db import models
from django.db.models import Q
from django.http import JsonResponse

settings.configure(
    ROOT_URLCONF=__name__,
    DEBUG=True,
    SECRET_KEY="secret",
    DATABASES={
		"default": {
			"ENGINE": "django.db.backends.sqlite3",
			"NAME" : "melon-20230906.sqlite3",
		},
	},
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": ["templates"],
        }
    ],
)
django.setup()


class Song(models.Model):
	id = models.AutoField(primary_key=True)
	가수 = models.CharField(max_length=100)
	곡명 = models.CharField(max_length=200)
	곡일련번호 = models.IntegerField()
	순위 = models.IntegerField()
	앨범 = models.CharField(max_length=200)
	좋아요 = models.IntegerField()
	커버이미지_주소 = models.URLField()

	def __str__(self):
		return self.곡명

	class Meta:
		db_table = "songs"
		app_label = "melon"


def index(request):
    return render(request, "index.html")


def song_list_api(request):
    query = request.GET.get("query", "").strip()  # 검색어

    song_list = Song.objects.all()  # QuerySet
    if query:
        song_list = song_list.filter(
            Q(곡명__icontains=query) | Q(가수__icontains=query)
        )

    song_list_data = list(song_list.values())

    return JsonResponse(
        song_list_data,
        safe=False,
        json_dumps_params={"ensure_ascii": False},
        content_type="application/json; charset=utf-8",
    )

urlpatterns = [
    path("", index),
    path("api/song-list.json", song_list_api),
]

execute_from_command_line(sys.argv)