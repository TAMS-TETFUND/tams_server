from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.serializer import AttendanceRecordSerializer, AttendanceSessionSerializer
from db.models import AttendanceRecord, AttendanceSession
from nodedevice.auth import NodeTokenAuth


class AttendanceList(APIView):
    authentication_classes = (NodeTokenAuth, )
    """List all students, or create a new student."""

    def get(self, request):
        attendance_record = AttendanceRecord.objects.all()
        serializer = AttendanceRecordSerializer(attendance_record, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AttendanceRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceSessionList(APIView):
    authentication_classes = (NodeTokenAuth, )
    """List all students, or create a new student."""

    def get(self, request):
        attendance_record = AttendanceSession.objects.all()
        serializer = AttendanceSessionSerializer(attendance_record, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AttendanceSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

