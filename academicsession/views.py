from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from db.models import AcademicSession
from academicsession.serializers import AcademicSessionSerializer
from nodedevice.auth import NodeTokenAuth


class AcademicSessionDetail(APIView):
    """Retrieve, update or delete a academic_session instance."""

    authentication_classes = (NodeTokenAuth,)

    def get_object(self, pk):
        try:
            return AcademicSession.objects.get(pk=pk)
        except AcademicSession.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        academic_session = self.get_object(pk)
        serializer = AcademicSessionSerializer(academic_session)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        academic_session = self.get_object(pk)
        serializer = AcademicSessionSerializer(
            academic_session, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        academic_session = self.get_object(pk)
        academic_session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AcademicSessionList(APIView):
    """List all academic sessions, or create a new academic_session."""

    authentication_classes = (NodeTokenAuth,)

    def get(self, request, format=None):
        academic_sessions = AcademicSession.objects.all()
        serializer = AcademicSessionSerializer(academic_sessions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AcademicSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
