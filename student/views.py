from django.core.management import call_command
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from db.models import Student
from student.serializers import StudentSerializer

import os
import json
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tams_server.settings")
application = get_wsgi_application()


class StudentDetail(APIView):
    """Retrieve, update or delete a student instance"""

    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        student = self.get_object(pk)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentList(APIView):
    """List all students, or create a new student."""

    def get(self, request, format=None):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentSyncView(APIView):
    def get(self, request):
        dump_file = 'server_dump.json'

        # dump the data in a file
        output = open(dump_file, 'w')  # Point stdout at a file for dumping data to.
        call_command('dumpdata', 'db', format='json', stdout=output)
        output.close()

        output = open(dump_file)  # reading the dumped data
        y = json.load(output)
        output.close()

        return Response(y)
