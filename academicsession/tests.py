from django.test import TestCase
from rest_framework.test import APIRequestFactory

from db.models import AcademicSession
from academicsession.views import AcademicSessionDetail, AcademicSessionList


class AcademicSessionListTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_academic_session_list(self):
        request = self.factory.get("academic-sessions/")
        response = AcademicSessionList.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_academic_session_creation(self):
        request = self.factory.post(
            "academic-sessions/", {"session": "2020/2021"}
        )
        response = AcademicSessionList.as_view()(request)
        self.assertEqual(response.status_code, 201)


class AcademicSessionDetailTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.session = AcademicSession.objects.create(id=1, session="2020/2021")

    def test_academic_session_detail(self):
        request = self.factory.get("academic-sessions/")
        response = AcademicSessionDetail.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_academic_session_detail_data(self):
        request = self.factory.get("academic-sessions/")
        response = AcademicSessionDetail.as_view()(request, pk=1)
        self.assertEqual(response.data["session"], "2020/2021")

    def test_academic_session_edit(self):
        request = self.factory.put(
            "academic-session/", {"session": "2021/2022"}
        )
        response = AcademicSessionDetail.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)

    def test_academic_session_edit_result(self):
        request = self.factory.put(
            "academic-session/", {"session": "2021/2022"}
        )
        response = AcademicSessionDetail.as_view()(request, pk=1)
        self.assertEqual(response.data["session"], "2021/2022")

    def test_academic_sesson_delete(self):
        request = self.factory.delete("academic-sessions/")
        response = AcademicSessionDetail.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 204)
