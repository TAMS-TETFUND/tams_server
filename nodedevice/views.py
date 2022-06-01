from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from nodedevice.models import NodeDevice
from nodedevice.serializers import NodeDeviceSerializer


class NodeDeviceDetail(APIView):
    """Retrieve, update or delete a node_device instance.
    """

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
    """List all node devices, or create a new node_device.
    """
    def get(self, request, format=None):
        node_devices = NodeDevice.objects.all()
        serializer = NodeDeviceSerializer(node_devices, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = NodeDeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)