"""tams_server URL Configuration"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from upload.views import populate_model, data_file_format

urlpatterns = [
    path("admin/", admin.site.urls),
    path("uploads/", populate_model, name="upload"),
    path("upload-format/", data_file_format, name="upload_format"),
    path("staff/", include("staff.urls")),
    path("students/", include("student.urls")),
    path("faculties/", include("faculty.urls")),
    path("departments/", include("department.urls")),
    path("academic-sessions/", include("academicsession.urls")),
    path("courses/", include("course.urls")),
    path("course-registrations/", include("courseregistration.urls")),
    path("node-devices/", include("nodedevice.urls")),
    path("api/v1/", include("djoser.urls")),
    path("api/v1/", include("djoser.urls.authtoken")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
