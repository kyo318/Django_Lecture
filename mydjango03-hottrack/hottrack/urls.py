from django.urls import path, re_path
from . import views

urlpatterns = [
    path(route="", view=views.index),
    path(route="<int:pk>/cover.png", view=views.cover_png),
    path(route="export.csv", view=views.export_csv),
    # 정규표현식을 통해 csv/xlsx 확장자의 주소만 허용합니다.
    re_path(
        route=r"^export\.(?P<format>(csv|xlsx))$", view=views.export, name="export"
    ),
]
