from django.test import TestCase

from main.json_views import StatusCollection
from main.models import StatusReport
from main.serializers import StatusReportSerializer

from payments.models import User

from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory


class JsonViewTests(TestCase):
    @classmethod
    def setUpClass(cls):  # only runs once
        super().setUpClass()
        cls.factory = APIRequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User(id=2222, email="test@user.com")
        cls.test_user.save()

    def get_request(self, method='GET', authed=True):
        request_method = getattr(self.factory, method.lower())
        request = request_method("")
        if authed:
            force_authenticate(request, self.test_user)

        return request

    def test_get_collection(self):
        status = StatusReport.objects.all()
        expected_json = StatusReportSerializer(status, many=True).data
        response = StatusCollection.as_view()(self.get_request())

        self.assertEquals(expected_json, response.data)

    def test_get_collection_requires_logged_in_user(self):
        anon_request = self.get_request(authed=False)
        response = StatusCollection.as_view()(anon_request)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
