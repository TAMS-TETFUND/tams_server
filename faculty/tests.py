from django.test import TestCase
from rest_framework.test import APIRequestFactory

from db.models import Faculty
from faculty.views import FacultyDetail, FacultyList


class FacultyListTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_faculty_list(self):
        request = self.factory.get('faculties/')
        response = FacultyList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_faculty_creation(self):
        request  = self.factory.post('faculties/', {"id":1, "name":"Engineering"})
        response = FacultyList.as_view()(request)
        self.assertEqual(response.status_code, 201)

    
class FacultyDetailTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.faculty = Faculty.objects.create(name="Engineering")
    
    def test_faculty_detail(self):
        request = self.factory.get('faculties/{}'.format(self.faculty.pk))
        response = FacultyDetail.as_view()(request, pk=self.faculty.pk)
        self.assertEqual(response.status_code, 200)

    def test_faculty_edit(self):
        faculty_api_fixture = {"id":self.faculty.pk, "name":"Applied Engineering"}
        request = self.factory.put('faculties/{}'.format(self.faculty.pk), faculty_api_fixture)
        response = FacultyDetail.as_view()(request, pk=self.faculty.pk)
        self.assertEqual(response.data["name"], faculty_api_fixture["name"])