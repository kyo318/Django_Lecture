from django.shortcuts import render
from django.contrib import messages


# Create your views here.
def index(request):
    messages.debug(request, message="디버그 레벨 메시지")
    messages.info(request, message="정보 레벨 메시지")
    messages.success(request, message="성공 레벨 메시지")
    messages.warning(request, message="경고 레벨 메시지")
    messages.error(request, message="에러 레벨 메시지")
    return render(request, template_name="core/index.html")
