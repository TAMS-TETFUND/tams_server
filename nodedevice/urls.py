from django.urls.conf import path

from nodedevice.views import NodeDeviceDetail, NodeDeviceList

app_name="nodedevice"

urlpatterns = [
    path("", NodeDeviceList.as_view()),
    path("<int:pk>/", NodeDeviceDetail.as_view()),
]
