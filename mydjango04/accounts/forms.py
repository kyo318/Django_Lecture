import datetime
from django import forms

from core.forms.widgets import PhoneNumberInput, DatePickerInput, NaverMapPointInput
from .models import Profile, User


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["address"].required = True

    class Meta:
        model = Profile
        fields = [
            "address",
            "phone_number",
            "photo",
            "birth_date",
            "location_point",
        ]
        widgets = {
            "phone_number": PhoneNumberInput,
            "birth_date": DatePickerInput,
            "location_point": NaverMapPointInput,
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]

    is_profile_update = forms.BooleanField(
        required=False,
        initial=True,
        label="프로필 수정 여부",
        help_text="체크 시 프로필 수정 단계를 생략합니다.",
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["address", "phone_number", "photo"]
