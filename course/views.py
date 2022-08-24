
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from db.models import Course
from course.serializers import CourseSerializer, CourseUpdateSerializer


class CourseDetail(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a course instance."""
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return CourseUpdateSerializer
        return CourseSerializer


class CourseList(ListCreateAPIView):
    """List all courses, or create a new course."""
    def get_queryset(self):
        queryset = Course.objects.all()
        department_name = self.request.query_params.get('department')
        if department_name is not None:
            queryset = queryset.filter(department__name=department_name)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CourseUpdateSerializer
        return CourseSerializer