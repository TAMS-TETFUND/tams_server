from django.urls.conf import path

from faculty.views import FacultyDetail, FacultyList

app_name = "faculty"

urlpatterns = [
    path("", FacultyList.as_view()),
    path("<int:pk>/", FacultyDetail.as_view()),
]
