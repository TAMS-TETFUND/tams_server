from django.test import TestCase
from rest_framework.test import APIRequestFactory

from db.models import Department, Faculty, Semester, Course
from course.views import CourseDetail, CourseList


class CourseListTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_course_list(self):
        request = self.factory.get('courses/')
        response = CourseList.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def test_course_creation(self):
        faculty = Faculty.objects.create(name="Engineering")
        department = Department.objects.create(name="ECE", faculty=faculty)
        request = self.factory.post(
            'courses/', 
            {
                "code": "ECE 371",
                "title": "System Programming",
                "level_of_study":1,
                "department":department.pk,
                "unit_load":3,
                "semester": Semester.FIRST
            }
        )
        response = CourseList.as_view()(request)
        self.assertEqual(response.status_code, 201)


class CourseDetailTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.faculty = Faculty.objects.create(name="Engineering")
        self.department = Department.objects.create(name="ECE", faculty=self.faculty)
        course_details = {
            "code": "ECE 371",
            "title": "System Programming",
            "level_of_study":1,
            "department":self.department,
            "unit_load":3,
            "semester": Semester.FIRST
        }
        self.course = Course.objects.create(**course_details)
    
    def test_course_detail(self):
        request = self.factory.get('courses/')
        response = CourseDetail.as_view()(request, pk=self.course.pk)
        self.assertEqual(response.status_code, 200)
    
    def test_course_edit(self):
        changed_course_title = {
            "id": self.course.pk,
            "code": "ECE 371",
            "title": "General Programming",
            "level_of_study":1,
            "department":self.department.pk,
            "unit_load":3,
            "semester": Semester.FIRST,
            "elective":False,
            "is_active":True
        }
        request = self.factory.put('courses/{}/'.format(self.course.pk), changed_course_title)
        response = CourseDetail.as_view()(request, pk=self.course.pk)
        self.assertEqual(response.status_code, 200)
    
    def test_course_edit_result(self):       
        changed_course_title = {
            "code": "ECE 371",
            "title": "General Programming",
            "level_of_study":1,
            "department":self.department.pk,
            "unit_load":3,
            "semester": Semester.FIRST
        }
        request = self.factory.put('courses/', changed_course_title)
        response = CourseDetail.as_view()(request, pk=self.course.pk)
        self.assertEqual(response.data["title"], changed_course_title["title"])