from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path(route="core/", view=include("core.urls")),
    path(route="blog/", view=include("blog.urls")),
    path("hottrack/", include("hottrack.urls")),
    path("", RedirectView.as_view(pattern_name="hottrack:index")),
    path("weblog/", include("weblog.urls")),
    path("shop/", include("shop.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
