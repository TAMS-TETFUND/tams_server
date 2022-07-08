from django.test import TestCase
from rest_framework.test import APIRequestFactory

from db.models import Department, Faculty, Student
from student.views import StudentDetail, StudentList
from tams_server.tests.fixtures import (
    faculty_fixture,
    department_fixture,
    student_fixture,
    student_api_fixture,
)


class StudentListTestCase(TestCase):
    """Tests for the StudentList api view"""

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_student_list(self):
        request = self.factory.get("students/")
        response = StudentList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_student_api_obj_creation(self):
        faculty = Faculty.objects.create(**faculty_fixture)
        department = Department.objects.create(**department_fixture)
        request = self.factory.post("students/", student_api_fixture)
        response = StudentList.as_view()(request)
        self.assertEqual(response.status_code, 201)


class StudentDetailTestCase(TestCase):
    """Tests for the StudentDetail api view"""

    def setUp(self):
        self.factory = APIRequestFactory()
        faculty = Faculty.objects.create(**faculty_fixture)
        department = Department.objects.create(**department_fixture)
        self.student = Student.objects.create(**student_fixture)

    def test_student_detail(self):
        request = self.factory.get("students/{}/".format(self.student.pk))
        response = StudentDetail.as_view()(request, pk=self.student.pk)
        self.assertEqual(response.status_code, 200)

    def test_student_detail_edit(self):
        modified_api_fixture = student_api_fixture
        modified_api_fixture["first_name"] = "Nicodemus"

        request = self.factory.put(
            "students/{}/".format(self.student.pk), modified_api_fixture
        )
        response = StudentDetail.as_view()(request, pk=self.student.pk)
        self.assertEqual(
            response.data["first_name"], modified_api_fixture["first_name"]
        )

    def test_student_delete(self):
        request = self.factory.delete("students/{}/".format(self.student.pk))
        response = StudentDetail.as_view()(request, pk=self.student.pk)
        self.assertEqual(response.status_code, 204)
