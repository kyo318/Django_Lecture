from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # path("<int:pk>/", view=views.post_detail, name="post_detail"),
    # path("<int:pk>/<str:slug>", view=views.post_detail, name="post_detail"),
    path("<slug>/", views.post_detail, name="post_detail"),
]
