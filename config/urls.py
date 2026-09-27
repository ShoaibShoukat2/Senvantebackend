from django.contrib import admin
from django.urls import include, path, re_path

from .frontend import spa

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("leads.urls")),
    re_path(r"^(?P<path>.*)$", spa),
]
