from typing import Dict, Optional
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import ProfileForm, UserForm, UserProfileForm
from accounts.models import Profile
from vanilla import UpdateView
from django.urls import reverse_lazy
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import default_storage
from django.contrib import messages


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


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy("accounts:profile_edit")

    def get_object(self):
        try:
            return self.request.user.profile
        except Profile.DoesNotExist:
            return None

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        return super().form_valid(form)


profile_edit = ProfileUpdateView.as_view()


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
