from django.urls.conf import path

from attendance.views import (
    AttendanceSessionByCourseList,
    AttendanceSessionByCourseDetail,
    AttendanceSessionList,
    StudentAttendanceList,
    download_attendance,
)

app_name = "attendance"

urlpatterns = [
    path("", AttendanceSessionList.as_view()),
    path("session/<str:pk>/", download_attendance, name="download_attendance"),
    path("by-course/", AttendanceSessionByCourseList.as_view()),
    path("by-course/detail/", AttendanceSessionByCourseDetail.as_view()),
    path("student-report/<path:student_id>", StudentAttendanceList.as_view()),
]
