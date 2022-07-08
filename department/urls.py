from django.urls.conf import path

from department.views import DepartmentDetail, DepartmentList

app_name = "department"

urlpatterns = [
    path("", DepartmentList.as_view()),
    path("<int:pk>/", DepartmentDetail.as_view()),
]
