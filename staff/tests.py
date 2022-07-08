from django.test import TestCase
from rest_framework.test import APIRequestFactory

from db.models import Department, Faculty, Staff, StaffTitle
from staff.views import StaffDetail, StaffList, StaffTitleDetail, StaffTitleList
from tams_server.tests.fixtures import (
    faculty_fixture,
    department_fixture,
    staff_title_fixture,
    staff_fixture,
    staff_api_fixture,
)


class StaffListTestCase(TestCase):
    """Tests for the StaffList api view"""

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_staff_list(self):
        request = self.factory.get("staff/")
        response = StaffList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_staff_api_obj_creation(self):
        faculty = Faculty.objects.create(**faculty_fixture)
        department = Department.objects.create(**department_fixture)
        staff_title = StaffTitle.objects.create(**staff_title_fixture)
        request = self.factory.post("staff/", staff_api_fixture)
        response = StaffList.as_view()(request)
        self.assertEqual(response.status_code, 201)


class StaffDetailTestCase(TestCase):
    """Tests for the StaffDetail api view"""

    def setUp(self):
        self.factory = APIRequestFactory()
        faculty = Faculty.objects.create(**faculty_fixture)
        department = Department.objects.create(**department_fixture)
        staff_title = StaffTitle.objects.create(**staff_title_fixture)

        self.staff_fixture = staff_fixture
        if "staff_titles" in self.staff_fixture:
            staff_obj_titles = self.staff_fixture.pop("staff_titles")
        self.staff = Staff.objects.create(**staff_fixture)

        self.staff_api_fixture = staff_api_fixture

    def test_staff_detail(self):
        request = self.factory.get("staff/{}/".format(self.staff.pk))
        response = StaffDetail.as_view()(request, pk=self.staff.pk)
        self.assertEqual(response.status_code, 200)

    def test_staff_detail_edit(self):
        self.staff_api_fixture["first_name"] = "James"
        request = self.factory.put(
            "staff/{}/".format(self.staff.pk), self.staff_api_fixture
        )
        response = StaffDetail.as_view()(request, pk=self.staff.pk)
        self.assertEqual(response.data["first_name"], "James")

    def test_staff_delete(self):
        request = self.factory.delete("staff/{}/".format(self.staff.pk))
        response = StaffDetail.as_view()(request, pk=self.staff.pk)
        self.assertEqual(response.status_code, 204)


class StaffTitleListTestCase(TestCase):
    """Tests for the StaffTitleList api view"""

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_staff_title_list(self):
        request = self.factory.get("staff/titles/")
        response = StaffTitleList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_staff_title_creation(self):
        request = self.factory.post("staff/titles/", staff_title_fixture)
        response = StaffTitleList.as_view()(request)
        self.assertEqual(response.status_code, 201)


class StaffTitleDetailTestCase(TestCase):
    """Tests for the StaffTitleDetail api view"""

    def setUp(self):
        self.factory = APIRequestFactory()
        self.staff_title = StaffTitle.objects.create(**staff_title_fixture)

    def test_staff_title_detail(self):
        request = self.factory.get(
            "staff/titles/{}/".format(self.staff_title.pk)
        )
        response = StaffTitleDetail.as_view()(request, pk=self.staff_title.pk)
        self.assertEqual(response.status_code, 200)

    def test_staff_title_edit(self):
        modified_staff_title_fixture = staff_title_fixture
        modified_staff_title_fixture[
            "title_full"
        ] = "Associate Professor/Reader"
        request = self.factory.put(
            "staff/titles/{}/".format(self.staff_title.pk),
            modified_staff_title_fixture,
        )
        response = StaffTitleDetail.as_view()(request, pk=self.staff_title.pk)
        self.assertEqual(
            response.data["title_full"],
            modified_staff_title_fixture["title_full"],
        )

    def test_staff_title_delete(self):
        request = self.factory.delete(
            "staff/titles/{}/".format(self.staff_title.pk)
        )
        response = StaffTitleDetail.as_view()(request, pk=self.staff_title.pk)
        self.assertEqual(response.status_code, 204)
