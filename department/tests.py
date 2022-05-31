from django.test import TestCase
from rest_framework.test import APIRequestFactory

from db.models import Department, Faculty
from department.views import DepartmentDetail, DepartmentList


class DepartmentListTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_department_list(self):
        request = self.factory.get('departments/')
        response = DepartmentList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_department_creation(self):
        self.faculty = Faculty.objects.create(name="Engineering")
        self.dept_api_fixture = {'id':1, 'name':'ECE', 'faculty':self.faculty.pk}
        request = self.factory.post('departments/', **self.dept_api_fixture)
        response = DepartmentList.as_view()(request)
        self.assertEqual(response.status_code, 201)


class DepartmentDetailTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.faculty = Faculty.objects.create(name="Engineering")
        self.dept_api_fixture = {'id':1, 'name':'ECE', 'faculty':self.faculty.pk}
        self.department = Department.objects.create(name="ECE", faculty=self.faculty)

    def test_department_detail(self):
        request = self.factory.get('departments/{}'.format(self.department.pk))
        response = DepartmentDetail.as_view()(request, pk=self.department.pk)
        self.assertEqual(response.status_code, 200)
    
    def test_department_edit(self):
        request = self.factory.put('departments/{}'.format(self.department.pk), {"id":self.department.pk, "name":"Electronic Engineering", "faculty": self.faculty.pk})
        response = DepartmentDetail.as_view()(request, pk=self.department.pk)
        self.assertEqual(response.data["name"], "Electronic Engineering")