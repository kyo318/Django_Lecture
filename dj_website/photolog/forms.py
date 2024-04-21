from typing import List
from django.core.files import File
from django import forms
from django.http import HttpRequest
from .models import Note, Photo, Comment
from django.core.checks import messages
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.forms import inlineformset_factory


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_clean(file) for file in data]
        else:
            single_clean(data)


class NoteForm(forms.ModelForm):
    photos = MultipleImageField(required=True)

    class Meta:
        model = Note
        fields = ["title", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {"novalidate": True}
        self.helper.layout = Layout("title", "content", "photos")
        self.helper.add_input(
            Submit(
                name="submit",
                value="저장하기",
                css_class="w-100",
            )
        )

    def clean_photos(self):
        is_required = self.fields["photos"].required

        file_list: List[File] = self.cleaned_data.get("photos")
        if not file_list and is_required:
            raise forms.ValidationError("최소 1개의 사진을 등록해주세요.")
        elif file_list:
            try:
                file_list = [Photo.make_thumb(file) for file in file_list]
            except Exception as e:
                raise forms.ValidationError(
                    "썸네일 생성 중에 오류가 발생했습니다."
                ) from e
        return file_list


class PhotoInlineForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image"]


PhotoUpdateFormSet = inlineformset_factory(
    parent_model=Note,
    model=Photo,
    form=PhotoInlineForm,
    extra=0,
    can_delete=True,
)
PhotoUpdateFormSet.helper = FormHelper()
PhotoUpdateFormSet.helper.form_tag = False


class NoteUpdateForm(NoteForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photos"].required = False
        self.helper.form_tag = False
        self.helper.inputs = []


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]

    def __init__(self, request:HttpRequest, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.attrs = {
            "hx-post": self.request.get_full_path(),
            "hx-trigger": "submit once",
            "hx-swap" : "outerHTML",
            "autocomplete": "off",
            "novalidate": True,
        }
        self.helper.layout = Layout("message")
        self.helper.label_class = "d-none"