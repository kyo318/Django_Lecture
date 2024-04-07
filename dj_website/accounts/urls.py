from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
]
