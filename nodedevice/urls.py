from django.urls.conf import path

from nodedevice.views import NodeDeviceDetail, NodeDeviceList, device_fixtures, NodeSyncView

app_name = "nodedevice"

urlpatterns = [
    path("", NodeDeviceList.as_view()),
    path("backup/id=<int:device_id>&token=<str:token>/", NodeSyncView.as_view()),
    path("<int:pk>/", NodeDeviceDetail.as_view()),
    path("init/", device_fixtures),
]
