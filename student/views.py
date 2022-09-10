from django.http import Http404

from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)
from rest_framework.response import Response
from rest_framework import status

from db.models import Department, Student
from nodedevice.auth import NodeTokenAuth
from student.serializers import StudentSerializer, StudentUpdateSerializer


class StudentDetail(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a student instance"""

    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return StudentUpdateSerializer
        return StudentSerializer


class StudentList(ListCreateAPIView):
    """List all students, or create a new student."""

    def get_queryset(self):
        queryset = Student.objects.all()
        department = self.request.query_params.get("department")
        faculty = self.request.query_params.get("faculty")

        # if department and faculty are passed filter based on the more
        # specific parameter: department
        if department is not None:
            queryset = queryset.filter(department__name__iexact=department)
        elif faculty is not None:
            queryset = queryset.filter(
                department__faculty__name__iexact=faculty
            )
        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return StudentUpdateSerializer
        return StudentSerializer
