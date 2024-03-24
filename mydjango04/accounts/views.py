from typing import Dict, Optional
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import ProfileForm, ProfileUserForm, UserForm, UserProfileForm
from accounts.models import Profile, User
from vanilla import UpdateView
from django.urls import reverse_lazy
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import default_storage
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator
from accounts.forms import SignupForm
from django.views.generic import CreateView
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from .forms import PasswordResetForm, SetPasswordForm

from django.contrib.auth.views import PasswordResetView as DjangoPasswordResetView
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm as DjangoSetPasswordForm
from django.contrib.auth.views import (
    PasswordResetConfirmView as DjangoPasswordResetConfirmView,
)

# from accounts.forms import PasswordChangeForm

# @login_required
# def profile_edit(request):
#     try:
#         instance = request.user.profile
#     except Profile.DoesNotExist:
#         instance = None
#     if request.method == "GET":
#         form = ProfileForm(instance=instance)
#     else:
#         form = ProfileForm(data=request.POST, files=request.FILES, instance=instance)
#         if form.is_valid():
#             profile = form.save(commit=False)
#             profile.user = request.user
#             profile.save()
#             return redirect("accounts:profile_edit")

#     return render(request, "accounts/profile_form.html", {"form": form})


@login_required
def profile_edit(request):
    try:
        instance = request.user.profile
    except Profile.DoesNotExist:
        instance = None

    if request.method == "GET":
        profile_user_form = ProfileUserForm(
            prefix="profile-user", instance=request.user
        )
        profile_form = ProfileForm(prefix="profile", instance=instance)
    else:
        profile_user_form = ProfileUserForm(
            prefix="profile-user",
            data=request.POST,
            files=request.FILES,
            instance=request.user,
        )
        profile_form = ProfileForm(
            prefix="profile", data=request.POST, files=request.FILES, instance=instance
        )
        if profile_user_form.is_valid() and profile_form.is_valid():
            profile_user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("accounts:profile_edit")

    return render(
        request,
        "accounts/profile_form.html",
        {
            "profile_user_form": profile_user_form,
            "profile_form": profile_form,
        },
    )


# class ProfileUpdateView(LoginRequiredMixin, UpdateView):
#     model = Profile
#     form_class = ProfileForm
#     success_url = reverse_lazy("accounts:profile_edit")

#     def get_object(self):
#         try:
#             return self.request.user.profile
#         except Profile.DoesNotExist:
#             return None

#     def form_valid(self, form):
#         profile = form.save(commit=False)
#         profile.user = self.request.user
#         return super().form_valid(form)


# profile_edit = ProfileUpdateView.as_view()


def check_is_profile_update(wizard_view: "UserProfileWizardView"):
    cleaned_date = wizard_view.get_cleaned_data_for_step("user_form")
    if cleaned_date is None:
        return True
    return cleaned_date.get("is_profile_update", False)


class UserProfileWizardView(LoginRequiredMixin, SessionWizardView):
    form_list = [
        ("user_form", UserForm),
        ("profile_form", UserProfileForm),
    ]
    # 임시 파일 스토리지 지정 : 폼에 파일필드가 있을 때 활용
    file_storage = default_storage
    template_name = "accounts/profile_wizard.html"

    condition_dict = {
        "profile_form": check_is_profile_update,
    }

    # 폼의 initial 인자를 설정할 수 있습니다.
    def get_form_initial(self, step: str) -> Dict:
        return {}

    # 폼의 instance 인자를 설정할 수 있습니다. (모델 폼에서만 호출됩니다.)
    def get_form_instance(self, step: str):
        if step == "user_form":  # 반드시 문자열 타입
            return self.request.user
        elif step == "profile_form":
            profile, __ = Profile.objects.get_or_create(user=self.request.user)
            return profile
        return super().get_form_instance(step)

    # 모든 단계가 완료되었을 때 호출되어, 응답 객체를 반환
    def done(self, form_list, form_dict, **kwargs) -> HttpResponse:
        # 각 Form을 저장하고, 다른 페이지로 이동합니다.
        user = form_dict["user_form"].save()
        if "profile_form" in form_dict:
            profile = form_dict["profile_form"].save(commit=False)
            profile.user = user
            profile.save()
        messages.success(self.request, "프로필을 저장했습니다.")
        return redirect("accounts:profile_wizard")


profile_wizard = UserProfileWizardView.as_view()


# def login(request):
#     if request.method == "GET":
#         return render(request, "accounts/login_form.html")
#     else:
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)
#         if user is None:
#             return HttpResponse("인증 실패", status=400)
#         request.session["_auth_user_id"] = user.pk
#         request.session["_auth_user_hash"] = user.get_session_auth_hash()
#         request.session["_auth_user_backend"] = user.backend

#         next_url = (
#             request.POST.get("next")
#             or request.GET.get("next")
#             or settings.LOGIN_REDIRECT_URL
#         )

#         return redirect(next_url)


def profile(request):
    return HttpResponse(
        f"username : {request.user.username}, {request.user.is_authenticated}"
    )


def signup(request):
    if request.method == "GET":
        form = SignupForm()
    else:
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            created_user = form.save()
            auth_login(request, created_user)

            next_url = request.POST.get("next") or request.GET.get("next")
            url_is_safe = url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            )

            if url_is_safe is False:
                next_url = ""
            # return redirect(settings.LOGIN_URL) # /accounts/login
            return redirect(next_url or settings.LOGIN_REDIRECT_URL)
    return render(
        request,
        "accounts/signup_form.html",
        {"form": form},
    )


# class SignupView(CreateView):
#     form_class = SignupForm
#     template_name = "accounts/signup_form.html"
#     success_url = settings.LOGIN_REDIRECT_URL

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         created_user = form.instance
#         auth_login(self.request, created_user)
#         return response

#     def get_success_url(self) -> str:
#         next_url = self.request.POST.get("next") or self.request.GET.get("next")
#         if next_url:
#             return next_url
#         return super().get_success_url()


# signup = SignupView.as_view()


# @csrf_protect
# @never_cache
# @require_POST
# def logout(request):
#     auth_logout(request)
#     next_url = request.GET.get("next")
#     if next_url:
#         url_is_safe = url_has_allowed_host_and_scheme(
#             url=next_url,
#             allowed_hosts={request.get_host()},
#             require_https=request.is_secure(),
#         )
#         if url_is_safe:
#             return redirect(next_url)
#     # return render(request, template_name="registration/logged_out.html")
#     return redirect(settings.LOGIN_URL)

logout = LogoutView.as_view(
    next_page=settings.LOGIN_URL,
)


class LoginView(DjangoLoginView):
    template_name = "accounts/login_form.html"
    redirect_authenticated_user = False


login = LoginView.as_view()


# @login_required
# def password_change(request):
#     if request.method == "GET":
#         form = PasswordChangeForm(request.user)
#     else:
#         form = PasswordChangeForm(request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "암호를 변경했습니다.")
#             # update_session_auth_hash(request, request.user)
#             return redirect("accounts:profile")
#     return render(request, "accounts/password_change_form.html", {"form": form})


class PasswordChangeView(DjangoPasswordChangeView):
    form_class = DjangoPasswordChangeForm
    sucess_url = reverse_lazy("accounts:prifle")
    template_name = "accounts/password_change_form.html"


password_change = PasswordChangeView.as_view()

# @csrf_protect
# def password_reset(request):
#     if request.method == "GET":
#         form = PasswordResetForm()
#     else:
#         form = PasswordResetForm(data=request.POST)
#         if form.is_valid():
#             form.save(request)
#             messages.success(
#                 request,
#                 (
#                     "비밀번호 재설정 메일을 발송하였습니다."
#                     "만약 이메일을 받지 못했다면 등록하신 이메일을 다시 확인하시거나 "
#                     "스팸 메일함을 확인해주시기 바랍니다."
#                 ),
#             )
#     return render(request, "registration/password_reset_form.html", {"form": form})


# def password_reset_confirm(request, uidb64, token):
#     uid = urlsafe_base64_decode(uidb64).decode()
#     user = get_object_or_404(User, pk=uid)

#     context_data = {}

#     reset_url_token = "set_password"

#     if token != reset_url_token:
#         if default_token_generator.check_token(user, token):
#             request.session["_password_reset_token"] = token
#             redirect_url = request.path.replace(token, reset_url_token)
#             return redirect(redirect_url)
#         else:
#             return render(
#                 request,
#                 "registration/password_reset_confirm.html",
#                 {"validlink": False},
#             )
#     else:
#         session_token = request.session.get("_password_reset_token")
#         if default_token_generator.check_token(user, session_token) is False:
#             validlink = False
#         else:
#             validlink = True
#             if request.method == "GET":
#                 form = SetPasswordForm(user=user)
#             else:
#                 form = SetPasswordForm(user=user, data=request.POST)
#                 if form.is_valid():
#                     form.save()
#                     del request.session["_password_reset_token"]
#                 post_reset_login = True
#                 if post_reset_login:
#                     auth_login(request, user)
#                     messages.success(
#                         request,
#                         message="암호를 재설정했으며, 자동 로그인 처리되었습니다.",
#                     )
#                     return redirect(settings.LOGIN_REDIRECT_URL)
#                 else:
#                     messages.success(
#                         request, message="암호를 재설정 했습니다. 로그인해주세요"
#                     )
#                     return redirect(settings.LOGIN_URL)
#             context_data["form"] = form

#         context_data["validlink"] = validlink

#         return render(
#             request,
#             "registration/password_reset_confirm.html",
#             context_data,
#         )


class PasswordResetConfirmView(DjangoPasswordResetConfirmView):
    success_url = settings.LOGIN_URL

    def form_valid(self, form):
        response = super().form_valid(form)

        messages.success(self.request, "암호를 재설정 했습니다.")
        return response


password_reset_confirm = PasswordResetConfirmView.as_view()


class PasswordResetView(DjangoPasswordResetView):
    email_template_name = "accounts/password_reset_email.html"
    success_url = reverse_lazy("accounts:password_reset")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            (
                "비밀번호 재설정 메일을 발송했습니다. 계정이 존재한다면 입력하신 이메일로 "
                "비밀번호 재설정 안내문을 확인하실 수 있습니다. "
                "만약 이메일을 받지 못했다면 등록하신 이메일을 다시 확인하시거나 스팸함을 확인해주세요."
            ),
        )
        return response


password_reset = PasswordResetView.as_view()
