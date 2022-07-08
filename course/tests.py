from django.test import TestCase
from rest_framework.test import APIRequestFactory

from db.models import Department, Faculty, Semester, Course
from course.views import CourseDetail, CourseList
from tams_server.tests import fixtures


class CourseListTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_course_list(self):
        request = self.factory.get("courses/")
        response = CourseList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_course_creation(self):
        faculty = Faculty.objects.create(**fixtures.faculty_fixture)
        department = Department.objects.create(**fixtures.department_fixture)
        request = self.factory.post("courses/", fixtures.course_api_fixture)
        response = CourseList.as_view()(request)
        self.assertEqual(response.status_code, 201)


class CourseDetailTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.faculty = Faculty.objects.create(**fixtures.faculty_fixture)
        self.department = Department.objects.create(
            **fixtures.department_fixture
        )

        self.course = Course.objects.create(**fixtures.course_fixture)

    def test_course_detail(self):
        request = self.factory.get("courses/")
        response = CourseDetail.as_view()(request, pk=self.course.pk)
        self.assertEqual(response.status_code, 200)

    def test_course_edit(self):
        changed_course_title = fixtures.course_api_fixture
        changed_course_title["title"] = "General Programming"
        request = self.factory.put(
            "courses/{}/".format(self.course.pk), changed_course_title
        )
        response = CourseDetail.as_view()(request, pk=self.course.pk)
        self.assertEqual(response.status_code, 200)

    def test_course_edit_result(self):
        changed_course_title = fixtures.course_api_fixture
        changed_course_title["title"] = "General Programming"
        request = self.factory.put("courses/", changed_course_title)
        response = CourseDetail.as_view()(request, pk=self.course.pk)
        self.assertEqual(response.data["title"], changed_course_title["title"])
