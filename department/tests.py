from django.test import TestCase
from rest_framework.test import APIRequestFactory

from db.models import Department, Faculty
from department.views import DepartmentDetail, DepartmentList
from tams_server.tests import fixtures


class DepartmentListTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_department_list(self):
        request = self.factory.get("departments/")
        response = DepartmentList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_department_creation(self):
        Faculty.objects.create(**fixtures.faculty_fixture)
        request = self.factory.post(
            "departments/", fixtures.department_api_fixture
        )
        response = DepartmentList.as_view()(request)
        self.assertEqual(response.status_code, 201)


class DepartmentDetailTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        Faculty.objects.create(**fixtures.faculty_fixture)
        self.department = Department.objects.create(
            **fixtures.department_fixture
        )

    def test_department_detail(self):
        request = self.factory.get("departments/{}".format(self.department.pk))
        response = DepartmentDetail.as_view()(request, pk=self.department.pk)
        self.assertEqual(response.status_code, 200)

    def test_department_edit(self):
        modified_dept_name = fixtures.department_api_fixture
        modified_dept_name["name"] = "Electronic and Robotics Engineeering"
        request = self.factory.put(
            "departments/{}".format(self.department.pk), modified_dept_name
        )
        response = DepartmentDetail.as_view()(request, pk=self.department.pk)
        self.assertEqual(response.data["name"], modified_dept_name["name"])
