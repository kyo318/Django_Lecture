from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import render, redirect
from weblog.forms import PostForm
from weblog.models import Post
from django.shortcuts import get_object_or_404
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from vanilla import FormView, CreateView, UpdateView
from django.views.generic import ListView, DeleteView
from .forms import ConfirmDeleteForm


# from django.views.generic import FormView
from django.http import HttpResponse


index = ListView.as_view(
    model=Post,
    template_name="weblog/index.html",
)


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("weblog:index")
    form_class = ConfirmDeleteForm


post_delete = PostDeleteView.as_view()


# def post_delete(request, pk):
#     instance = get_object_or_404(Post, pk=pk)

#     if request.method == "GET":
#         return render(request, "weblog/post_confirm_delete.html", {"post": instance})
#     else:
#         instance.delete()
#         return redirect("weblog:post_new")


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "weblog/post_detail.html", {"post": post})


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = "weblog/post_form.html"
    success_url = "/"

    def form_valid(self, form) -> HttpResponse:
        self.object = form.save(commit=False)
        self.object.ip = self.request.META["REMOTE_ADDR"]
        # post.save()
        # form.save_m2m()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return resolve_url(self.object)


post_new = PostCreateView.as_view()


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "weblog/post_form.html"
    success_url = "/weblog/"

    # def get_form(self, data=None, files=None, **kwargs):
    #     post_pk = self.kwargs["pk"]
    #     instance = get_object_or_404(Post, pk=post_pk)
    #     kwargs["instance"] = instance
    #     return super().get_form(data=data, files=files, **kwargs)

    # def form_valid(self, form):
    #     form.save(commit=True)
    #     return super().form_valid()


post_edit = PostUpdateView.as_view()
# Create your views here.
# def post_new(request):
#     if request.method == "GET":
#         form = PostForm()
#     else:
#         form = PostForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             print("form.cleaned_data :", form.cleaned_data)
#             not_saved_instance = form.save(commit=False)
#             # 모델 인스턴스만 생성하고, .save() 메서드는 호출하지 않습니다.
#             not_saved_instance.ip = request.META["REMOTE_ADDR"]
#             # 이제 데이터베이스로의 저장을 시도
#             not_saved_instance.save()
#             form.save_m2m()
#         return redirect("/")

#     return render(request, "weblog/post_form.html", {"form": form})


# def post_edit(request, pk):
#     instance = get_object_or_404(Post, pk=pk)
#     if request.method == "GET":
#         form = PostForm(instance=instance)
#     else:
#         form = PostForm(data=request.POST, files=request.FILES, instance=instance)
#         if form.is_valid():
#             post = form.save(commit=True)
#             return redirect("/")
#         else:
#             pass

#     return render(
#         request,
#         "weblog/post_form.html",
#         {
#             "form": form,
#         },
#     )
