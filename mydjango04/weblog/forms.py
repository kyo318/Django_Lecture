from django import forms
from weblog.models import Post
from core.forms.widgets import (
    CounterTextInput,
    IosSwitchInput,
    PreviewClearableFileInput,
)


# class PostForm(forms.Form):
#     title = forms.CharField()
#     content = forms.CharField(widget=forms.Textarea)
#     status = forms.ChoiceField(
#         choices=[
#             ("D", "초안"),
#             ("P", "발행"),
#         ]
#     )
#     photo = forms.ImageField(required=False)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "status", "photo", "tag_set", "is_public"]
        widgets = {
            "title": CounterTextInput,
            "is_public": IosSwitchInput,
            "photo": PreviewClearableFileInput,
        }


class ConfirmDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        label="동의",
        help_text="삭제에 동의하시면 체크해주세요.",
        required=True,
    )
