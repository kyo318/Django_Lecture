from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from photolog.models import Note, Photo
from photolog.forms import NoteForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    note_qs = Note.objects.all().select_related("author").prefetch_related("photo_set")
    return render(
        request,
        "photolog/index.html",
        {"note_list": note_qs},
    )


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "crispy_form.html"
    extra_context = {"form_title": "새 기록"}
    success_url = reverse_lazy("photolog:index")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        new_note = self.object
        new_note.author = self.request.user
        new_note.save()

        photo_file_list = form.cleaned_data.get("photos")
        if photo_file_list:
            Photo.create_photos(new_note, photo_file_list)

        messages.success(self.request, message="새 기록을 저장했습니다.")
        return redirect(self.get_success_url())


note_new = NoteCreateView.as_view()
