import csv
from datetime import datetime

from django.http import (
    Http404,
    HttpResponse,
    HttpResponseServerError,
    HttpResponseForbidden,
)
from django.db.models import Q, F
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from rest_framework import status
from academicsession.serializers import AcademicSessionSerializer

from attendance.serializers import (
    AttendanceRecordSerializer,
    AttendanceSessionSerializer,
)
from course.serializers import CourseSerializer
from student.serializers import StudentSerializer

from db.models import (
    AcademicSession,
    AttendanceRecord,
    AttendanceSession,
    Course,
    Student,
)


def download_attendance(request, pk):
    attendance_session = AttendanceSession.objects.get(id=pk)

    if (
        attendance_session.initiator is None
        or attendance_session.initiator.username != request.user.username
    ):
        return HttpResponseForbidden(
            "403: Permission Denied %s here" % request.user.username
        )

    qs = (
        AttendanceRecord.objects.filter(
            Q(
                Q(attendance_session=attendance_session)
                & Q(attendance_session__initiator_id=request.user.username)
            )
        )
        .prefetch_related("student")
        .values(
            "student__first_name",
            "student__last_name",
            "student__reg_number",
            "student__department",
            "student__department__name",
            "student__department__faculty",
            "check_in_by",
        )
    )
    if request.method == "POST":
        if "faculty" in request.POST:
            qs = qs.filter(student__faculty=request.POST["faculty"])
        if "department" in request.POST:
            qs = qs.filter(student__department=request.POST["department"])

    if not qs.exists():
        return HttpResponseServerError("Error: No records found")

    response = HttpResponse(
        content_type="text/csv",
        headers={
            f"Content-Disposition": "attachment; filename="
            f"{attendance_session.course.code} "
            f'Attendance {datetime.strftime(attendance_session.start_time, "%d-%m-%Y")}.csv'
        },
    )

    field_names = ["S/N", "Name", "Reg. Number", "Department", "Sign In"]
    attendance_writer = csv.DictWriter(response, fieldnames=field_names)
    attendance_writer.writerow(
        {
            "S/N": f'{attendance_session.course.code} Attendance {datetime.strftime(attendance_session.start_time, "%d-%m-%Y")}'
        }
    )
    attendance_writer.writeheader()
    for idx, row in enumerate(qs, 1):
        attendance_writer.writerow(
            {
                "S/N": idx,
                "Name": f'{row["student__last_name"].capitalize()} {row["student__first_name"].capitalize()}',
                "Reg. Number": row["student__reg_number"],
                "Department": row["student__department__name"],
                "Sign In": f'{datetime.strftime(row["check_in_by"], "%H:%M")}',
            }
        )

    return response


class AttendanceSessionPagination(PageNumberPagination):
    page_size = 15


class AttendanceSessionList(generics.ListCreateAPIView):
    """Lists all attendance sessions belonging to user making request"""

    ordering_fields = ["session__session", "course"]
    pagination_class = AttendanceSessionPagination
    serializer_class = AttendanceSessionSerializer

    def get_queryset(self):
        sessions_with_records = set(
            AttendanceRecord.objects.values_list(
                "attendance_session", flat=True
            )
        )
        return AttendanceSession.objects.filter(
            initiator__isnull=False,
            id__in=sessions_with_records,
            initiator_id=self.request.user.username,
        ).order_by('-start_time')


class AttendanceSessionByCourseList(generics.ListAPIView):
    """Lists all attendance sessions for all courses the user making request has
    ever initiated an attendance for.
    """
    serializer_class = AttendanceSessionSerializer

    def get_queryset(self):
        sessions_with_records = set(AttendanceRecord.objects.values_list("attendance_session", flat=True))
        courses_by_sessions = list(
            AttendanceSession.objects.filter(id__in=sessions_with_records, initiator_id=self.request.user.username)
            .values("course", "session")
            .distinct()
        )
        qs = []
        for course in courses_by_sessions:
            qs.append(
                AttendanceSession.objects.exclude(
                    initiator__isnull=True
                ).filter(**course)
            )
        # join all the courses for which the user has created an attendance
        # session for
        all_attendance_sessions = None
        if qs:
            all_attendance_sessions = qs[0].union(*qs[1:])
        return all_attendance_sessions


class AttendanceSessionByCourseDetail(APIView):
    """Gives a breakdown of student attendance rates for a course."""
    def get(self, request):
        context = {}
        course = request.query_params.get('course')
        session = request.query_params.get('session')

        course_data = CourseSerializer(Course.objects.get(pk=course), many=False)
        context['course'] = course_data.data

        session_data = AcademicSessionSerializer(AcademicSession.objects.get(pk=session), many = False)
        context['session'] = session_data.data


        all_records = AttendanceRecord.objects.filter(attendance_session__course__id=course, attendance_session__session__id=session)

        students = set(all_records.values_list('student', flat=True))
        attendance_details = []
        for student in students:
            attendance_details.append({
                "student": StudentSerializer(Student.objects.get(pk=student)).data,
                "valid_check_ins": AttendanceRecordSerializer(all_records.filter(student_id=student, is_valid=True), many=True).data
            })

        context['student_attendance'] = attendance_details

        return Response(context)



class AttendanceList(APIView):
    # authentication_classes = (NodeTokenAuth,)
    """List all students, or create a new student."""

    def get(self, request):
        attendance_record = AttendanceRecord.objects.all()
        serializer = AttendanceRecordSerializer(attendance_record, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AttendanceRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentAttendanceList(APIView):
    """
    List all attendance sessions for courses a student attended at
    least a lecture for.
    """

    def get(self, request, student_id, session=None):
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Http404

        # all the courses student attended a lecture for in every semester
        student_attended_events_list = list(
            AttendanceRecord.objects.filter(student=student)
            .values(
                "attendance_session__course__id",
                "attendance_session__session__id",
            )
            .distinct()
        )
        print("student: ", student.reg_number)
        print(
            "this is student's attendance list: ", student_attended_events_list
        )
        student_attendance_report = []

        for event in student_attended_events_list:
            item = {}
            item["academic_session"] = AcademicSessionSerializer(
                AcademicSession.objects.get(
                    id=event["attendance_session__session__id"]
                ),
                many=False,
            ).data
            item["course"] = CourseSerializer(
                Course.objects.get(id=event["attendance_session__course__id"]),
                many=False,
            ).data

            item["events"] = AttendanceSessionSerializer(
                AttendanceSession.objects.filter(
                    session_id=event["attendance_session__session__id"],
                    course_id=event["attendance_session__course__id"],
                ),
                many=True,
            ).data

            item["student_records"] = AttendanceRecordSerializer(
                AttendanceRecord.objects.filter(student=student, **event),
                many=True,
            ).data
            student_attendance_report.append(item)
        return Response(student_attendance_report)


