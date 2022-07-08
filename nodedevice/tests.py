import re

from rest_framework.test import APIRequestFactory
from django.test import TestCase

from db.models import NodeDevice
from nodedevice.views import NodeDeviceDetail, NodeDeviceList


class NodeDeviceTestCase(TestCase):
    def test_node_device_model_creation(self):
        node_device = NodeDevice.objects.create()
        self.assertTrue(re.match("^TAMS ", node_device.name) is not None)


class NodeDeviceListTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_node_device_list(self):
        request = self.factory.get("node-devices/")
        response = NodeDeviceList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_node_device_api_creation(self):
        request = self.factory.post(
            "node-devices/",
            {"name": NodeDevice.next_device_name(NodeDevice.next_valid_id())},
        )
        response = NodeDeviceList.as_view()(request)
        self.assertEqual(response.status_code, 201)


class NodeDeviceDetailTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.node_device = NodeDevice.objects.create()

    def test_node_device_detail(self):
        request = self.factory.get("node-devices/")
        response = NodeDeviceDetail.as_view()(request, pk=self.node_device.pk)
        self.assertEqual(response.status_code, 200)

    def test_node_device_edit(self):
        changed_device_name = {
            "id": self.node_device.pk,
            "name": "New Name",
            "token": self.node_device.token,
        }
        request = self.factory.put("node-devices/", changed_device_name)
        response = NodeDeviceDetail.as_view()(request, pk=self.node_device.pk)
        self.assertEqual(response.data["name"], changed_device_name["name"])
