from rest_framework import serializers

from db.models import Faculty, Student, Department


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ["id", "name"]


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(many=False, read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "alias", "faculty"]


class StudentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(many=False, read_only=True)

    class Meta:
        model = Student
        fields = [field.name for field in Student._meta.fields]