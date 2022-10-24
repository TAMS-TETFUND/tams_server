from datetime import datetime

from django.db import IntegrityError
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from openpyxl.writer.excel import save_virtual_workbook

from academicsession.serializers import AcademicSessionSerializer
from attendance.serializers import (
    AttendanceRecordCreationSerializer,
    AttendanceRecordSerializer,
    AttendanceSessionCreationSerializer,
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
from .spreadsheets import generate_attendance_records_sheet


@api_view(["GET"])
def download_attendance(request, pk):
    attendance_session = AttendanceSession.objects.get(id=pk)

    # if (
    #     attendance_session.initiator is None
    #     or attendance_session.initiator.username != request.user.username
    # ):
    #     return HttpResponseForbidden("403: Permission Denied")

    qs = (
        AttendanceRecord.objects.filter(attendance_session=attendance_session)
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

    wb = generate_attendance_records_sheet(attendance_session, qs)

    response = HttpResponse(
        content=save_virtual_workbook(wb),
        content_type="application/ms-excel",
        headers={
            f"Content-Disposition": "attachment; filename="
            f"{attendance_session.course.code} "
            f'Attendance {datetime.strftime(attendance_session.start_time, "%d-%m-%Y")}.xlsx'
        },
    )
    return response


def download_collated_attendance(request):
    """
    This view is for processing and returning a CSV file of collated attendance
    for a course the user making the request has initiated an attendance for.

    get all attendance sessions for a course in the given session,
    get all the students that ever attended an event for the course,
    for each student check attedance for every attendance session list from step one
    """
    course = request.query_params.get("course")
    session = request.query_params.get("session")
    if course is None or session is None:
        return HttpResponseBadRequest(
            "Invalid request: specify course and session"
        )

    if not (course_obj := Course.objects.filter(pk=course)).exists():
        return Http404("Course does not exist")
    if not (session_obj := AcademicSession.objects.filter(pk=session)).exists():
        return Http404("Academic Session does not exist")

    course_obj = course_obj.first()
    session_obj = session_obj.first()

    all_course_events = AttendanceSession.objects.filter(
        course=course_obj, session=session_obj
    ).order_by("-start_time")
    course_events_list = all_course_events.values_list("id", flat=True)
    all_attendance_records = AttendanceRecord.objects.filter(
        attendance_session__in=course_events_list
    )
    students_in_attendance = set(
        all_attendance_records.order_by("-student__last_name").values_list(
            "student__reg_number",
            "student__first_name",
            "student_last_name",
            "student__department__name",
            "student__level_of_study",
        )
    )
    attendance_tally = {}

    for student in students_in_attendance:
        student_tally = []
        for event in course_events_list:
            if AttendanceRecord.objects.filter(
                student_id=student[0], attendance_session=event
            ).exists():
                student_tally.append("PRESENT")
            else:
                student_tally.append("ABSENT")
        attendance_tally[student] = student_tally

    response = HttpResponse(
        content_type="text/csv",
        headers={
            f"Content-Disposition": "attachment; filename="
            f"{course_obj.code} {session_obj.session} Collated Attendance.csv"
        },
    )

    # field_names = ["Reg_number", "Name"] + [session_date for session_date in ]


class AttendanceSessionPagination(PageNumberPagination):
    page_size = 15


class AttendanceSessionList(generics.ListCreateAPIView):
    """Lists all attendance sessions belonging to user making request"""

    ordering_fields = ["session__session", "course"]
    pagination_class = AttendanceSessionPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AttendanceSessionCreationSerializer
        return AttendanceSessionSerializer

    def get_queryset(self):
        sessions_with_records = set(
            AttendanceRecord.objects.values_list(
                "attendance_session", flat=True
            )
        )
        print("rest_framework knows the user is: ", self.request.user.username)
        return AttendanceSession.objects.filter(
            initiator__isnull=False,
            id__in=sessions_with_records,
            initiator_id=self.request.user.username,
        ).order_by("-start_time")

    def create(self, request, *args, **kwargs):
        """Create method that can allow a post request of list of AttendanceSession objects."""
        if not isinstance(request.data, list):
            return super(AttendanceSessionList, self).create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AttendanceSessionByCourseList(generics.ListAPIView):
    """Lists all attendance sessions for all courses the user making request has
    ever initiated an attendance for.
    """

    serializer_class = AttendanceSessionSerializer

    def get_queryset(self):
        sessions_with_records = set(
            AttendanceRecord.objects.values_list(
                "attendance_session", flat=True
            )
        )
        courses_by_sessions = list(
            AttendanceSession.objects.filter(
                id__in=sessions_with_records,
                initiator_id=self.request.user.username,
            )
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
        course = request.query_params.get("course")
        session = request.query_params.get("session")

        course_data = CourseSerializer(
            Course.objects.get(pk=course), many=False
        )
        context["course"] = course_data.data

        session_data = AcademicSessionSerializer(
            AcademicSession.objects.get(pk=session), many=False
        )
        context["session"] = session_data.data

        all_records = AttendanceRecord.objects.filter(
            attendance_session__course__id=course,
            attendance_session__session__id=session,
        )

        all_sessions = AttendanceSessionSerializer(
            AttendanceSession.objects.filter(
                course_id=course, session_id=session
            ).order_by("start_time"),
            many=True,
        )
        context["all_sessions"] = all_sessions.data

        students = set(all_records.values_list("student", flat=True))
        attendance_details = []
        for student in students:
            attendance_details.append(
                {
                    "student": StudentSerializer(
                        Student.objects.get(pk=student)
                    ).data,
                    "valid_check_ins": AttendanceRecordSerializer(
                        all_records.filter(student_id=student, is_valid=True),
                        many=True,
                    ).data,
                }
            )

        context["student_attendance"] = attendance_details

        return Response(context)


class AttendanceList(APIView):
    # authentication_classes = (NodeTokenAuth,)
    """List all students, or create a new student."""

    def get(self, request):
        attendance_record = AttendanceRecord.objects.all()
        serializer = AttendanceRecordSerializer(attendance_record, many=True)
        return Response(serializer.data)

    def post(self, request):
        if type(request.data) != list:
            response = {"details": "Invalid data type!"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        for record_data in request.data:
            serializer = AttendanceRecordCreationSerializer(data=record_data)
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            try:
                serializer.save()
            except IntegrityError:
                continue

        response = {"details": "successfully synced"}
        return Response(response, status=status.HTTP_201_CREATED)


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
