from django.urls.conf import path

from academicsession.views import AcademicSessionDetail, AcademicSessionList

app_name = "academicsession"

urlpatterns = [
    path("", AcademicSessionList.as_view()),
    path("<int:pk>/", AcademicSessionDetail.as_view()),
]
