from rest_framework import serializers

from db.models import (
    AttendanceRecord,
    AttendanceSession,
    AttendanceSessionStatusChoices,
    EventTypeChoices,
    Staff,
    Student,
)
from course.serializers import CourseSerializer
from academicsession.serializers import AcademicSessionSerializer


class AttendanceSessionSerializer(serializers.ModelSerializer):
    initiator = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.all(), many=False
    )
    course = CourseSerializer(many=False, read_only=True)
    session = AcademicSessionSerializer(many=False, read_only=True)
    event_type_detail = serializers.SerializerMethodField()
    status_detail = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceSession
        fields = "__all__"

    def get_event_type_detail(self, obj, choices=EventTypeChoices):
        return EventTypeChoices(obj.event_type).label

    def get_status_detail(self, obj, choices=AttendanceSessionStatusChoices):
        return AttendanceSessionStatusChoices(obj.status).label


class AttendanceRecordSerializer(serializers.ModelSerializer):
    attendance_session = serializers.PrimaryKeyRelatedField(
        queryset=AttendanceRecord.objects.all(), many=False
    )
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), many=False
    )

    class Meta:
        model = AttendanceRecord
        fields = "__all__"
