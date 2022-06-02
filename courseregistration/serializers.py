from rest_framework import serializers

from db.models import CourseRegistration, AcademicSession, Student, Course


class CourseRegistrationSerializer(serializers.ModelSerializer):
    session = serializers.PrimaryKeyRelatedField(queryset=AcademicSession.objects.all(), many=False)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=False)
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=False)

    class Meta:
        model = CourseRegistration
        fields = "__all__"
