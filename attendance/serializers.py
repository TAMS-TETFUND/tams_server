from rest_framework import serializers

from db.models import AttendanceSessionStatus, AttendanceRecord, AttendanceSession, Staff, AcademicSession, Course, Student
from course.serializers import CourseSerializer
from academicsession.serializers import AcademicSessionSerializer


class AttendanceSessionSerializer(serializers.ModelSerializer):
    initiator = serializers.PrimaryKeyRelatedField(queryset=Staff.objects.all(), many=False)
    course = CourseSerializer(many=False, read_only=True)
    session = AcademicSessionSerializer(many=False, read_only=True)
    status = serializers.IntegerField(choices=AttendanceSessionStatus.choices)

    class Meta:
        model = AttendanceSession
        fields = "__all__"


class AttendanceRecordSerializer(serializers.ModelSerializer):
    attendance_session = serializers.PrimaryKeyRelatedField(queryset=AttendanceRecord.objects.all(), many=False)
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=False)

    class Meta:
        model = AttendanceRecord
        fields = "__all__"