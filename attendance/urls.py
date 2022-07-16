from django.urls.conf import path

from attendance.views import AttendanceSessionList

app_name="attendance"

urlpatterns = [
    path("", AttendanceSessionList.as_view()),
]