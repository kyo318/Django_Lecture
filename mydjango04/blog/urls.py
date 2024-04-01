from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    # path("<int:pk>/", view=views.post_detail, name="post_detail"),
    # path("<int:pk>/<str:slug>", view=views.post_detail, name="post_detail"),
    path(
        "posts/premium-user-guide/", views.premium_user_guide, name="premium_user_guide"
    ),
    path(
        "posts/premium/<str:slug>/",
        views.post_premium_detail,
        name="posts/post_premium_detail",
    ),
    path("posts/search/", views.search, name="search"),
    path("posts/new/", views.post_new),
    path("posts/<str:slug>/", views.post_detail, name="post_detail"),
    path("posts/", views.post_list, name="post_list"),
    path("reviews/new", views.review_new, name="review_new"),
    path("reviews/", views.review_list, name="review_list"),
    path("reviews/<int:pk>/", views.review_detail, name="review_detail"),
    path("reviews/<int:pk>/edit", views.review_edit, name="review_edit"),
    path("demo/", views.demo_form, name="demo_form"),
    path("memogroup/<int:group_pk>/form/", views.memo_form, name="memo_form"),
    path("tags/", views.tag_list, name="tag_list"),
    path("tags/new/", views.tag_new, name="tag_new"),
    path("test/", views.test, name="test"),
    path("tags/<int:pk>/delete/", views.tag_delete, name="tag_delete"),
    path("tags/<int:pk>/edit/", views.tag_edit, name="tag_edit"),
    path("tags/item/<int:pk>/", views.tag_list_item, name="tag_list_item"),
]
