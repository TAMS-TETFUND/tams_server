import csv
from datetime import datetime

from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.db.models import Q, F
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response

from db.models import (
    AttendanceRecord,
    AttendanceSession,
)
from attendance.serializers import AttendanceSessionSerializer


def download_attendance(request, pk):
    attendance_session = AttendanceSession.objects.get(id=pk)

    if (
        attendance_session.initiator is None
        or attendance_session.initiator.username != request.user.username
    ):
        return HttpResponseForbidden("403: Permission Denied")

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
            "logged_by",
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
                "Sign In": f'{datetime.strftime(row["logged_by"], "%H:%M")}',
            }
        )

    return response


class AttendanceSessionList(APIView):
    """Lists all attendance sessions belonging to user making request"""

    def get(self, request, format=None):
        attendance_sessions = AttendanceSession.objects.filter(initiator_id=request.user.id)
        serializer = AttendanceSessionSerializer(attendance_sessions, many=True)
        return Response(serializer.data)


class AttendanceSessionByCourseList(APIView):
    """Lists all attendance sessions for a course the user making request has
        ever initiated an attendance for.
    """
    def get(self, request, format=None):
        courses_by_sessions = list(AttendanceSession.objects.filter(initiator_id=request.user.id).values("course", "session").distinct())
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

