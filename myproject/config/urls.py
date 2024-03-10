from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    # path(route="MatSimDB/", view=include("MatSimDB.urls")),
    # path(route="", view=lambda request: redirect("MatSimDB/")),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
