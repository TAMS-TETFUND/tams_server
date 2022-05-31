from rest_framework import serializers

from db.models import Department, Faculty
from faculty.serializers import FacultySerializer


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = serializers.PrimaryKeyRelatedField(queryset=Faculty.objects.all(),many=False)
    class Meta:
        model = Department
        fields = '__all__'