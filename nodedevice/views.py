import json
import os

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from db.models import NodeDevice, Student, Staff, Course
from db.datasynch import dump_data
from nodedevice.auth import NodeTokenAuth
from nodedevice.serializers import NodeDeviceSerializer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tams_server.settings")
application = get_wsgi_application()


# @api_view(['GET'])
# def device_fixtures(request):
#     """Get data to be used to populate new device db."""
#     if request.method == 'GET':
#         data = dump_data()
#         # try:
#         #     json.loads(data)
#         # except ValueError as e:
#         #     return Response("Error getting data: %s" % e , status=status.HTTP_400_BAD_REQUEST)
#         # else:
#         return Response(json.dumps(data), status.HTTP_200_OK)


def device_fixtures(request):
    """Get data to be used to populate new device db."""
    data = dump_data()
    return JsonResponse(json.dumps(data), safe=False)


class NodeDeviceDetail(APIView):
    """Retrieve, update or delete a node_device instance."""

    def get_object(self, pk):
        try:
            return NodeDevice.objects.get(pk=pk)
        except NodeDevice.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        node_device = self.get_object(pk)
        serializer = NodeDeviceSerializer(node_device)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        node_device = self.get_object(pk)
        serializer = NodeDeviceSerializer(node_device, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        node_device = self.get_object(pk)
        node_device.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class NodeDeviceList(APIView):
    """List all node devices, or create a new node_device."""
    authentication_classes = (NodeTokenAuth,)

    def get(self, request, format=None):
        node_devices = NodeDevice.objects.all()
        serializer = NodeDeviceSerializer(node_devices, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NodeDeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            node = NodeDevice.objects.get(id=int(serializer.data['id']))
            response = {
                "id": node.id,
                "token": node.token,
            }

            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NodeSyncView(APIView):
    def get(self, request):
        files = (
            os.path.join('dumps', 'staff_dump.json'),
            os.path.join('dumps', 'student_dump.json'),
            os.path.join('dumps', 'student_course.json'),
        )

        db = (
            "db.staff",
            "db.student",
            "db.course",
        )

        # Staff filter
        with open(files[0], 'w') as output:
            call_command("dump_object", db[0], [i.pk for i in Staff.objects.filter(is_exam_officer=False)],
                         stdout=output)

        # Student filter
        with open(files[1], 'w') as output:
            call_command("dump_object", db[1], [i.pk for i in Student.objects.filter(is_active=True)],
                         stdout=output)
        # course filter
        with open(files[2], 'w') as output:
            call_command("dump_object", db[2], [i.pk for i in Course.objects.all()],
                         stdout=output)

        # merge json files while removing duplicate values
        output = []
        seen = set()

        for f in files:
            f = open(f)
            data = json.loads(f.read())
            for obj in data:
                key = '%s|%s' % (obj['model'], obj['pk'])
                if key not in seen:
                    seen.add(key)
                    output.append(obj)
            f.close()

        return Response(output)
