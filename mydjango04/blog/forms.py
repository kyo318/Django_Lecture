from django import forms
from .models import Memo, Review, Tag
from core.forms.widgets import StarRatingSelect
from django.core.validators import MinLengthValidator, MaxLengthValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Field
from crispy_forms.bootstrap import PrependedText, TabHolder, Tab
from crispy_bootstrap5.bootstrap5 import FloatingField
from core.crispy_bootstrap5_ext.layout import BorderedTabHolder
from django.db import models


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["message", "rating"]
        widgets = {
            "rating": StarRatingSelect(choices=[(i, i) for i in range(1, 6)]),
        }


class DemoForm(forms.Form):
    author = forms.CharField(label="작성자")
    instagram_username = forms.CharField(label="인스타그램 아이디")
    title = forms.CharField(label="제목")
    summary = forms.CharField(
        label="요약",
        help_text="본문에 대한 요약을 최소 20자, 최대 200자 내로 입력해주세요.",
        validators=[MinLengthValidator(20), MaxLengthValidator(200)],
    )
    content = forms.CharField(widget=forms.Textarea, label="내용")
    content_en = forms.CharField(widget=forms.Textarea, label="내용(영문)")

    field_order = ["title", "author", "summary", "instagram_username"]

    def clean(self):
        content = self.cleaned_data.get("content")
        summary = self.cleaned_data.get("summary")

        if content and not summary:
            raise forms.ValidationError("본문에 대한 요약을 입력해주세요.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            FloatingField("title"),
            FloatingField("summary"),
            BorderedTabHolder(
                Tab("내용", "content"),
                Tab("내용(영문)", "content_en"),
            ),
            Row(
                Field("author", wrapper_class="col-sm-6"),
                PrependedText("instagram_username", "@", wrapper_class="col-sm-6"),
            ),
        )
        self.helper.attrs = {"novalidate": True}
        self.helper.add_input(Submit("submit", "제출"))

    # helper = FormHelper()
    # helper.form_action = ""  # action 속성
    # helper.form_tag = True  # form 태그 자동 생성
    # helper.disable_csrf = False  # csrf token 자동 추가
    # helper.attrs = {"novalidate": True}  # form 태그에 추가할 속성
    # helper.add_input(Submit("submit", "제출"))  # submit 버튼 추가


# class MemoForm(forms.Form):
#     class Status(models.TextChoices):
#         PRIVATE = "V", "비공개"
#         PUBLIC = "P", "공개"

#     message = forms.CharField(
#         max_length=140,
#         widget=forms.TextInput(attrs={"placeholder": "메모를 입력하세요."}),
#     )
#     status = forms.ChoiceField(initial=Status.PUBLIC, choices=Status.choices)


class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ["message", "status"]


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
