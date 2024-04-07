from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.forms import LoginForm, ProfileForm, SignupForm
from accounts.models import Profile, User
from accounts.utils import send_welcome_email
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import RedirectURLMixin  # type: ignore
from django.contrib.auth.mixins import LoginRequiredMixin


class SignupView(RedirectURLMixin, CreateView):
    model = User
    form_class = SignupForm
    template_name = "crispy_form.html"
    extra_context = {
        "form_title": "회원가입",
    }
    success_url = reverse_lazy("accounts:login")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            redirect_to = self.success_url
            if redirect_to != request.path:
                messages.warning(request, "로그인 유저는 회원가입을 할 수 없습니다.")
                return HttpResponseRedirect(redirect_to)  # type: ignore

        response = super().dispatch(request, *args, **kwargs)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, message="회원가입을 환영합니다.")
        user = self.object
        auth_login(self.request, user)
        messages.success(self.request, message="로그인 되었습니다.")
        send_welcome_email(user)
        return response


signup = SignupView.as_view()


class LoginView(DjangoLoginView):
    redirect_authenticated_user = True
    form_class = LoginForm
    template_name = "crispy_form.html"
    extra_context = {
        "form_title": "로그인",
    }


login = LoginView.as_view()


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


class LogoutView(DjangoLogoutView):
    next_page = "accounts:login"

    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, message="로그아웃 했습니다.")
        return response


logout = LogoutView.as_view()


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "프로필 수정"}
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated:
            return None
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            return None

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, message="프로필을 저장하였습니다.")
        return response


profile_edit = ProfileUpdateView.as_view()
