from rest_framework import serializers

from db.models import Department, Student
from department.serializers import DepartmentSerializer


class StudentSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), many=False
    )

    class Meta:
        model = Student
        fields = "__all__"
