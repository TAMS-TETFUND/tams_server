from django.urls.conf import path

from attendance.views import AttendanceSessionByCourseList, AttendanceSessionList, download_attendance

app_name="attendance"

urlpatterns = [
    path("", AttendanceSessionList.as_view()),
    path("session/<int:pk>/", download_attendance, name="download_attendance"),
    path("by-course/", AttendanceSessionByCourseList.as_view()),
]