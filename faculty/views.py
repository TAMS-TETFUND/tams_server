from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from db.models import Faculty
from faculty.serializers import FacultySerializer


class FacultyDetail(APIView):
    """Retrieve, update or delete a faculty instance.
    """

    def get_object(self, pk):
        try:
            return Faculty.objects.get(pk=pk)
        except Faculty.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        faculty = self.get_object(pk)
        serializer = FacultySerializer(faculty)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        faculty = self.get_object(pk)
        serializer = FacultySerializer(faculty, data=request.data)    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        faculty = self.get_object(pk)
        faculty.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FacultyList(APIView):
    """List all faculties, or create a new faculty.
    """
    def get(self, request, format=None):
        faculties = Faculty.objects.all()
        serializer = FacultySerializer(faculties, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = FacultySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
