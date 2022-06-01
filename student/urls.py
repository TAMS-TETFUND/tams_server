from django.urls.conf import path

from student.views import StudentDetail, StudentList

app_name="student"

urlpatterns = [
    path("", StudentList.as_view()),
    path("<int:pk>/", StudentDetail.as_view()),
]
