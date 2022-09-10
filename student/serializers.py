from rest_framework import serializers

from db.models import AdmissionStatusChoices, Department, SexChoices, Student
from department.serializers import DepartmentSerializer


class StudentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(many=False, read_only=True)
    admission_status_detail = serializers.SerializerMethodField()
    sex_detail = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = "__all__"

    def get_admission_status_detail(self, obj, choices=AdmissionStatusChoices):
        return AdmissionStatusChoices(obj.admission_status).label

    def get_sex_detail(self, obj, choices=SexChoices):
        return SexChoices(obj.sex).label


class StudentUpdateSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), many=False
    )

    class Meta:
        model = Student
        fields = "__all__"
