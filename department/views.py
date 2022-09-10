from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from db.models import Department
from department.serializers import (
    DepartmentSerializer,
    DepartmentUpdateSerializer,
)


class DepartmentDetail(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a department instance."""

    queryset = Department.objects.all()

    def get_serializer_class(self):
        if self.request.method in ("PUT", "PATCH"):
            return DepartmentUpdateSerializer
        return DepartmentSerializer


class DepartmentList(ListCreateAPIView):
    """List all departments, or create a new department."""

    def get_queryset(self):
        queryset = Department.objects.all()
        faculty_name = self.request.query_params.get("faculty")
        if faculty_name is not None:
            queryset = queryset.filter(faculty__name__iexact=faculty_name)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DepartmentUpdateSerializer
        return DepartmentSerializer
