from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # path("<int:pk>/", view=views.post_detail, name="post_detail"),
    # path("<int:pk>/<str:slug>", view=views.post_detail, name="post_detail"),
    path("premium-user-guide/", views.premium_user_guide, name="premium_user_guide"),
    path("premium/<str:slug>/", views.post_premium_detail, name="post_premium_detail"),
    path("<str:slug>/", views.post_detail, name="post_detail"),
    path("", views.post_list, name="post_list"),
]
