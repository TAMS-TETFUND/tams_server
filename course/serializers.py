from rest_framework import serializers

from db.models import Course, Department
from department.serializers import DepartmentSerializer


class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseUpdateSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), many=False
    )

    class Meta:
        model = Course
        fields = "__all__"
