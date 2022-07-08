from django.urls.conf import path

from course.views import CourseDetail, CourseList

app_name = "course"

urlpatterns = [
    path("", CourseList.as_view()),
    path("<int:pk>/", CourseDetail.as_view()),
]
