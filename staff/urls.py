from django.urls.conf import path

from staff.views import StaffDetail, StaffList, StaffTitleDetail, StaffTitleList

app_name = "staff"

urlpatterns = [
    path("", StaffList.as_view()),
    path("<int:pk>/", StaffDetail.as_view()),
    path("titles/", StaffTitleList.as_view()),
    path("titles/<int:pk>", StaffTitleDetail.as_view()),
]
