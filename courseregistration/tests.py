from django.test import TestCase
from rest_framework.test import APIRequestFactory

from db.models import Course, AcademicSession, CourseRegistration, Department, Faculty, Semester, Student
from courseregistration.views import CourseRegistrationDetail, CourseRegistrationList
from tams_server.tests import fixtures

class CourseRegistrationListTestCase(TestCase):
    """Tests for CoureRegistrationList api view"""
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_course_registration_list(self):
        request = self.factory.get('course-registrations/')
        response = CourseRegistrationList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_course_registration_api_obj_creation(self):
        Faculty.objects.create(**fixtures.faculty_fixture)
        Department.objects.create(**fixtures.department_fixture)
        AcademicSession.objects.create(**fixtures.academic_session_fixture)
        Course.objects.create(**fixtures.course_fixture)
        Student.objects.create(**fixtures.student_fixture)
        
        request = self.factory.post('course-registrations/', fixtures.course_registration_api_fixture)
        response = CourseRegistrationList.as_view()(request)
        self.assertEqual(response.status_code, 201)


class CourseRegistrationDetailTestCase(TestCase):
    """Tests for CourseRegistrationDetail api view"""

    def setUp(self):
        self.factory = APIRequestFactory()
        Faculty.objects.create(**fixtures.faculty_fixture)
        Department.objects.create(**fixtures.department_fixture)
        AcademicSession.objects.create(**fixtures.academic_session_fixture)
        Course.objects.create(**fixtures.course_fixture)
        Student.objects.create(**fixtures.student_fixture)

        self.course_reg = CourseRegistration.objects.create(**fixtures.course_registration_fixture)
    
    def test_course_registration_detail(self):
        request = self.factory.get('course-registrations/{}/'.format(self.course_reg.pk))
        response = CourseRegistrationDetail.as_view()(request, pk=self.course_reg.pk)

        self.assertEqual(response.status_code, 200)

    def test_course_registration_delete(self):
        request = self.factory.delete('course-registrations/{}/'.format(self.course_reg.pk))
        response = CourseRegistrationDetail.as_view()(request, pk=self.course_reg.pk)

        self.assertEqual(response.status_code, 204)