from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.core.files import File
from django.urls import reverse_lazy
from vanilla import CreateView, FormView, UpdateView
from accounts.forms import UserForm, UserProfileForm
from accounts.models import Profile, User
from blog.models import Memo, MemoGroup, Post, Review
from blog.forms import DemoForm, ReviewForm, MemoForm
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth import get_user_model


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
    query = request.GET.get("query", "").strip()

    post_qs = Post.objects.all()
    if query:
        post_qs = post_qs.filter(
            Q(title__icontains=query) | Q(tag_set__name__in=[query])
        )
    post_qs = post_qs.select_related("author")
    post_qs = post_qs.prefetch_related("tag_set")
    return render(
        request,
        "blog/post_list.html",
        {
            "query": query,
            "post_list": post_qs,
        },
    )


def search(request):
    query = request.GET.get("query", "").strip()
    return render(
        request=request,
        template_name="blog/search.html",
        context={
            "query": query,
        },
    )


def post_new(request):
    message: str = request.POST.get("message", "")
    photo: File = request.FILES.get("photo", "")
    errors = {"message": [], "photo": []}
    if not message:
        errors["message"].append("message 필드는 필수 필드 입니다.")
    if len(message) < 10:
        errors["message"].append("message 필드를 10글자 이상이어야 합니다.")
    if not photo:
        errors["photo"].append("photo 필드는 필수 필드 입니다.")
    if photo and not photo.name.lower().endswith((".jpg", ".jpeg")):
        errors["photo"].append("jpg 파일만 업로드 할 수 있습니다.")
    return render(
        request=request,
        template_name="blog/post_new.html",
        context={
            "message": message,
            "photo": photo,
            "errors": errors,
        },
    )


review_list = ListView.as_view(model=Review)

review_detail = DetailView.as_view(model=Review)

review_edit = UpdateView.as_view(
    model=Review,
    form_class=ReviewForm,
)
review_new = CreateView.as_view(
    model=Review,
    form_class=ReviewForm,
)

demo_form = FormView.as_view(
    form_class=DemoForm,
    template_name="blog/demo_form.html",
)


# memo_new = FormView.as_view(
#     form_class=MemoForm,
#     template_name="blog/memo_form.html",
#     success_url=reverse_lazy("blog:memo_new"),
# )
# def memo_new(request):
#     MemoFormSet = formset_factory(
#         form=MemoForm,
#         extra=3,
#     )
#     if request.method == "GET":
#         formset = MemoFormSet()

#     else:
#         print(request.POST)
#         formset = MemoFormSet(data=request.POST, files=request.FILES)

#         if formset.is_valid():

#             memo_list = []
#             for form in formset:
#                 if form.has_changed():
#                     memo = Memo(
#                         message=form.cleaned_data["message"],
#                         status=form.cleaned_data["status"],
#                     )
#                     memo_list.append(memo)

#             objs = Memo.objects.bulk_create(memo_list)

#             print("formset.cleaned_data :", formset.cleaned_data)
#             messages.success(request, f"메모 {len(objs)}개를 입력받았습니다.")
#             return redirect("blog:memo_new")

#     return render(
#         request,
#         "blog/memo_form.html",
#         {
#             "formset": formset,
#         },
#     )


@login_required
def memo_form(request, group_pk):
    MemoFormSet = inlineformset_factory(
        parent_model=MemoGroup,
        model=Memo,
        form=MemoForm,
    )

    memo_group = get_object_or_404(MemoGroup, pk=group_pk)
    queryset = None
    if request.method == "GET":
        formset = MemoFormSet(queryset=queryset, instance=memo_group)
    else:
        formset = MemoFormSet(
            data=request.POST,
            files=request.FILES,
            queryset=queryset,
            instance=memo_group,
        )
        if formset.is_valid():
            objs = formset.save()

            if objs:
                messages.success(request, f"메모 {len(objs)}개를 저장했습니다")
            if formset.deleted_objects:
                messages.success(
                    request, f"메모 {len(formset.deleted_objects)}개를 삭제했습니다"
                )
            return redirect("blog:memo_form", group_pk)
    return render(
        request,
        "blog/memo_form.html",
        {
            "formset": formset,
            "memo_group": memo_group,
        },
    )


@login_required
def profile_edit(request):
    user_instance = request.user
    try:
        profile_instance = request.user.profile
    except Profile.DoesNotExist:
        profile_instance = None
    if request.method == "GET":
        user_form = UserForm(prefix="user", instance=user_instance)
        profile_form = UserProfileForm(
            prefix="profile",
            instance=profile_instance,
        )
    else:
        user_form = UserForm(
            prefix="user",
            instance=user_instance,
            data=request.POST,
            files=request.FILES,
        )

        profile_form = UserProfileForm(
            prefix="profile",
            instance=profile_instance,
            data=request.POST,
            files=request.FILES,
        )
    if user_form.is_valie() and profile_form.is_valid():
        user_form.save()
        profile = profile_form.save(commit=False)
        profile.user = request.user
        profile.save()
        return redirect("accounts:profile_edit")
    return render(
        request,
        "accounts/profile_form.html",
        {
            "profile_form": profile_form,
        },
    )
