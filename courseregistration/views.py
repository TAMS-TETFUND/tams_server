from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from db.models import CourseRegistration
from courseregistration.serializers import CourseRegistrationSerializer


class CourseRegistrationDetail(APIView):
    """Retrieve or delete a course_registration instance.
    """

    def get_object(self, pk):
        try:
            return CourseRegistration.objects.get(pk=pk)
        except CourseRegistration.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        course_registration = self.get_object(pk)
        serializer = CourseRegistrationSerializer(course_registration)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        course_registration = self.get_object(pk)
        course_registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseRegistrationList(APIView):
    """List all course registrations, or create a new courseregistration.
    """
    def get(self, request, format=None):
        course_registrations = CourseRegistration.objects.all()
        serializer = CourseRegistrationSerializer(course_registrations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CourseRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
