from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve
from contact.views import contact


class ContactPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = '/contact/'
        cls.request = RequestFactory().get(cls.url)
        cls.request.session = 1

    def test_contact_page_resolves_to_right_view(self):
        contact_page = resolve(self.url)

        self.assertEquals(contact_page.func, contact)

    # def test_contact_page_returns_appropriate_status_code(self):
    #     contact_page = self.client.get(self.url)
    #
    #     self.assertEquals(contact_page.status_code, 200)
