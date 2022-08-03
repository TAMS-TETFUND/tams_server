import csv
from datetime import datetime

from django.http import Http404, HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.db.models import Q, F
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status

from attendance.serializer import AttendanceRecordSerializer, AttendanceSessionSerializer
from course.serializers import CourseSerializer
from nodedevice.auth import NodeTokenAuth

from db.models import (
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
        return HttpResponseForbidden("403: Permission Denied %s here"%request.user.username)

    qs = (
        AttendanceRecord.objects.filter(
            Q(
                Q(attendance_session=attendance_session)
                & Q(attendance_session__initiator=request.user)
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

    field_names = ["S/N", "Name", "Reg. Number","Department", "Sign In"]
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
                "Department":  row["student__department__name"],
                "Sign In": f'{datetime.strftime(row["check_in_by"], "%H:%M")}',
            }
        )

    return response


class AttendanceSessionList(APIView):
    """Lists all attendance sessions belonging to user making request"""
    authentication_classes = (NodeTokenAuth, )

    def get(self, request, format=None):
        attendance_sessions = AttendanceSession.objects.filter(initiator_id=request.user.username)
        serializer = AttendanceSessionSerializer(attendance_sessions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AttendanceSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceSessionByCourseList(APIView):
    """Lists all attendance sessions for a course the user making request has
        ever initiated an attendance for.
    """
    def get(self, request, format=None):
        courses_by_sessions = list(AttendanceSession.objects.filter(initiator_id=request.user.username).values("course", "session").distinct())
        qs = []
        for course in courses_by_sessions:
            qs.append(AttendanceSession.objects.exclude(initiator__isnull=True).filter(**course))
        # join all the courses for which the user has created an attendance 
        # session for
        all_attendance_sessions = None
        if qs:
            all_attendance_sessions = qs[0].union(*qs[1:])

        serializer = AttendanceSessionSerializer(all_attendance_sessions, many=True)
        return Response(serializer.data)




class AttendanceList(APIView):
    authentication_classes = (NodeTokenAuth, )
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
            AttendanceRecord.objects.filter(student=student).values(
                "attendance_session__course__id", 
                "attendance_session__session__id"
            ).distinct()
        )
        print("student: ", student.reg_number)
        print("this is student's attendance list: ", student_attended_events_list)
        student_attendance_report = []

        for event in student_attended_events_list:
            item = {}

            item['course'] = CourseSerializer(
                Course.objects.get(
                    id=event["attendance_session__course__id"]
                ), 
                many=False
            ).data
            
            item['events'] = AttendanceSessionSerializer(
                AttendanceSession.objects.filter(
                    session_id=event["attendance_session__session__id"], 
                    course_id=event["attendance_session__course__id"]
                ), 
                many=True
            ).data
            
            item['student_records'] = AttendanceRecordSerializer(AttendanceRecord.objects.filter(student=student, **event), many=True).data
            student_attendance_report.append(item)
            print("got here")
        return Response(student_attendance_report)