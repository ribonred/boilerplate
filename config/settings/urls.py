from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))  # type: ignore
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))  # type: ignore
