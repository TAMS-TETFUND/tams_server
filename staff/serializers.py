from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from db.models import Staff, StaffTitle


class StaffTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffTitle
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    staff_titles = PrimaryKeyRelatedField(
        required=False, queryset=StaffTitle.objects.all(), many=True
    )
    password = serializers.CharField(max_length=128, required=False)

    class Meta:
        model = Staff
        fields = "__all__"

    def create(self, validated_data):
        staff_no = validated_data.get("username")
        instance = Staff.objects.filter(staff_number=staff_no).first()

        if instance is not None:
            return instance

        instance = Staff(**validated_data)
        instance.set_password(validated_data.get("password"))
        instance.save()
        return instance
