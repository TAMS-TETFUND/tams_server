from urllib import request
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from db.models import Staff, StaffTitle
from staff.serializers import StaffSerializer, StaffTitleSerializer


class StaffDetail(APIView):
    """Retrieve, update, or delete a staff instance."""

    def get_object(self, pk):
        try:
            return Staff.objects.get(pk=pk.upper())
        except Staff.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        staff = self.get_object(pk.upper())
        serializer = StaffSerializer(staff)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        staff = self.get_object(pk.upper())
        serializer = StaffSerializer(staff, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        staff = self.get_object(pk.upper())
        staff.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffList(APIView):
    """List all staff, or create a new staff."""

    def get(self, request, format=None):
        staff_objs = Staff.objects.all()
        serializer = StaffSerializer(staff_objs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffTitleDetail(APIView):
    """Retrieve, update, or delete a staff title instance."""

    def get_object(self, pk):
        try:
            return StaffTitle.objects.get(pk=pk)
        except StaffTitle.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        staff_title = self.get_object(pk)
        serializer = StaffTitleSerializer(staff_title)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        staff_title = self.get_object(pk)
        serializer = StaffTitleSerializer(staff_title, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        staff_title = self.get_object(pk)
        staff_title.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffTitleList(APIView):
    """List all staff titles, or create a new staff title."""

    def get(self, request, format=None):
        staff_titles = StaffTitle.objects.all()
        serializer = StaffTitleSerializer(staff_titles, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StaffTitleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
