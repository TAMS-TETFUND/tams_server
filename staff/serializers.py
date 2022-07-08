from rest_framework import serializers

from db.models import Department, Staff, StaffTitle
from department.serializers import DepartmentSerializer


class StaffTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffTitle
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), many=False
    )
    staff_titles = serializers.PrimaryKeyRelatedField(
        queryset=StaffTitle.objects.all(), many=True
    )

    class Meta:
        model = Staff
        fields = "__all__"
