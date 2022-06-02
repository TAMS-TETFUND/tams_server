from django.urls.conf import path

from courseregistration.views import CourseRegistrationDetail, CourseRegistrationList

app_name="courseregistration"

urlpatterns = [
    path("", CourseRegistrationList.as_view()),
    path("<int:pk>/", CourseRegistrationDetail.as_view()),
]
