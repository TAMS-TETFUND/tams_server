"""tams_server URL Configuration"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from upload.views import populate_model, data_file_format
from home.views import vue_mount


urlpatterns = [
    path("", vue_mount, name="home"),
    path("api/v1/admin/uploads/", populate_model, name="upload"),
    path("api/v1/admin/upload-format/", data_file_format, name="upload_format"),
    path("api/v1/admin/", admin.site.urls),
    path("api/v1/staff/", include("staff.urls")),
    path("api/v1/students/", include("student.urls")),
    path("api/v1/faculties/", include("faculty.urls")),
    path("api/v1/departments/", include("department.urls")),
    path("api/v1/academic-sessions/", include("academicsession.urls")),
    path("api/v1/attendance/", include("attendance.urls")),
    path("api/v1/courses/", include("course.urls")),
    path("api/v1/course-registrations/", include("courseregistration.urls")),
    path("api/v1/node-devices/", include("nodedevice.urls")),
    path("api/v1/", include("djoser.urls")),
    path("api/v1/", include("djoser.urls.authtoken")),
    path("api/v1/accounts/", include("django.contrib.auth.urls")),
]
# including login and logout views for the browsable API.
urlpatterns += [
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.VUE_IMG_URL, document_root=settings.VUE_IMG_ROOT)

# let vue handle all other url patterns not specified here
urlpatterns += [
    re_path("^.", vue_mount)
]