from rest_framework import serializers

from db.models import Course, Department


class CourseSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), many=False)

    class Meta:
        model = Course
        fields = "__all__"
