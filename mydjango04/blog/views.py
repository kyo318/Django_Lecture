from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.
@login_required
@permission_required("blog.view_post", raise_exception=False)
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return HttpResponse(f"{post.pk}번 글의 {post.slug}")


@login_required
@permission_required("blog.view_premium_post", login_url="blog:premium_user_guide")
def post_premium_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return HttpResponse(f"프리미엄 컨텐츠 페이지 : {post.slug}")


def premium_user_guide(request):
    return HttpResponse("프리미엄 유저 가이드 페이지")


def post_list(request):
    post_qs = Post.objects.all()
    post_qs = post_qs.select_related("author")
    return render(
        request,
        "blog/post_list.html",
        {
            "post_list": post_qs,
        },
    )
